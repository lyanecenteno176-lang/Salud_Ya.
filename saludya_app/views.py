from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils.text import slugify
from .models import (
    Habit,
    HabitEntry,
    ProgressRecord,
    Badge,
    GamificationProfile,
    PointTransaction,
    Challenge,
    UserChallenge,
    Reward,
    RewardRedemption,
    MarketplaceCategory,
    Product,
    ProductReview,
    Coupon,
    Cart,
    CartItem,
    Order,
    OrderItem,
)
import json
import datetime


def _escape_pdf_text(text):
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def _build_simple_pdf(lines):
    escaped_lines = [_escape_pdf_text(str(line)) for line in lines]
    content = 'BT /F1 14 Tf 72 760 Td (' + escaped_lines[0] + ') Tj'
    for line in escaped_lines[1:]:
        content += ' 0 -18 Td (' + line + ') Tj'
    content += ' ET'
    content_bytes = content.encode('latin-1')

    header = b'%PDF-1.4\n'
    obj1 = b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'
    obj2 = b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n'
    obj3 = b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n'
    obj4 = b'4 0 obj\n<< /Length ' + str(len(content_bytes)).encode('latin-1') + b' >>\nstream\n' + content_bytes + b'\nendstream\nendobj\n'
    obj5 = b'5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n'

    objects = [header, obj1, obj2, obj3, obj4, obj5]
    offsets = []
    cursor = 0
    for obj in objects:
        offsets.append(cursor)
        cursor += len(obj)

    body = b''.join(objects)
    xref = b'xref\n0 6\n0000000000 65535 f \n'
    for offset in offsets[1:]:
        xref += f'{offset:010d} 00000 n \n'.encode('latin-1')
    startxref = len(body)
    trailer = b'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n' + str(startxref).encode('latin-1') + b'\n%%EOF\n'
    return body + xref + trailer


def index(request):
    return render(request, 'saludya_app/Index.html')


def registro(request):
    return render(request, 'saludya_app/registro.html')


def config_agua(request):
    return render(request, 'saludya_app/config-agua.html')


def config_ejercicios(request):
    return render(request, 'saludya_app/config-ejercicios.html')


def config_medicinas(request):
    return render(request, 'saludya_app/config-medicinas.html')


def perfil(request):
    return render(request, 'saludya_app/perfil.html')

def _get_profile(user):
    profile, created = GamificationProfile.objects.get_or_create(user=user)
    return profile


def _unlock_badge(user, name, description, icon='🏅'):
    badge, created = Badge.objects.get_or_create(user=user, name=name, defaults={
        'description': description,
        'icon': icon,
        'achieved': True,
        'date_awarded': datetime.date.today(),
    })
    if not created and not badge.achieved:
        badge.achieved = True
        badge.date_awarded = datetime.date.today()
        badge.save()
    return badge


def _award_points(user, amount, reason, entry=None):
    profile = _get_profile(user)
    profile.points_total += amount
    if profile.points_total >= profile.next_badge_target:
        profile.level += 1
        profile.next_badge_target += 100
        _unlock_badge(user, f'Level {profile.level}', f'Has alcanzado el nivel {profile.level}', icon='🥇')
    profile.save()
    PointTransaction.objects.create(
        user=user,
        habit_entry=entry,
        points=amount,
        reason=reason,
    )
    return profile


def _update_challenges(user, habit_type, date):
    active_challenges = UserChallenge.objects.filter(user=user, challenge__habit_type=habit_type, completed=False)
    for user_challenge in active_challenges:
        if user_challenge.last_activity_date == date:
            continue
        if user_challenge.last_activity_date == date - datetime.timedelta(days=1):
            user_challenge.days_completed += 1
        else:
            user_challenge.days_completed = 1
        user_challenge.last_activity_date = date
        if user_challenge.days_completed >= user_challenge.challenge.target_days:
            user_challenge.completed = True
            user_challenge.completed_at = date
            _award_points(user, user_challenge.challenge.reward_points, f'Completó reto {user_challenge.challenge.name}')
            _unlock_badge(user, f'Reto {user_challenge.challenge.name}', user_challenge.challenge.description, icon='🏆')
        user_challenge.save()


def progreso(request):
    user = request.user if request.user.is_authenticated else None
    habits = Habit.objects.filter(user=user, active=True) if user else Habit.objects.none()
    entries = HabitEntry.objects.filter(habit__user=user).order_by('-date')[:10] if user else HabitEntry.objects.none()
    badges = Badge.objects.filter(user=user, achieved=True) if user else Badge.objects.none()
    progress_records = ProgressRecord.objects.filter(user=user).order_by('-date')[:4] if user else ProgressRecord.objects.none()
    profile = _get_profile(user) if user else None
    badge_progress = int((profile.points_total / profile.next_badge_target) * 100) if profile and profile.next_badge_target else 0
    challenges = UserChallenge.objects.filter(user=user, completed=False) if user else UserChallenge.objects.none()
    rewards = Reward.objects.filter(active=True)

    context = {
        'habits': habits,
        'entries': entries,
        'badges': badges,
        'progress_records': progress_records,
        'profile': profile,
        'badge_progress': badge_progress,
        'challenges': challenges,
        'rewards': rewards,
    }
    return render(request, 'saludya_app/progreso.html', context)


def gamification_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = _get_profile(request.user)
    badge_progress = int((profile.points_total / profile.next_badge_target) * 100) if profile.next_badge_target else 0
    badges = Badge.objects.filter(user=request.user, achieved=True)
    challenges = UserChallenge.objects.filter(user=request.user, completed=False)
    rewards = Reward.objects.filter(active=True)

    context = {
        'profile': profile,
        'badge_progress': badge_progress,
        'badges': badges,
        'challenges': challenges,
        'rewards': rewards,
    }
    return render(request, 'saludya_app/gamification_dashboard.html', context)


def redeem_reward(request, reward_id):
    if not request.user.is_authenticated:
        return redirect('index')

    reward = get_object_or_404(Reward, pk=reward_id, active=True)
    profile = _get_profile(request.user)
    if profile.points_total < reward.cost_points or reward.stock <= 0:
        return JsonResponse({'status': 'error', 'message': 'Puntos insuficientes o recompensa agotada.'}, status=400)

    profile.points_total -= reward.cost_points
    profile.save()

    reward.stock -= 1
    reward.save()

    redemption = RewardRedemption.objects.create(
        user=request.user,
        reward=reward,
        points_spent=reward.cost_points,
        status='completed',
        completed_at=datetime.datetime.now(),
    )

    return JsonResponse({
        'status': 'ok',
        'message': f'Recompensa "{reward.name}" canjeada con éxito.',
        'points_total': profile.points_total,
    })


def habit_create(request):
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        data = request.POST
        Habit.objects.create(
            user=request.user,
            name=data.get('name'),
            habit_type=data.get('habit_type'),
            daily_goal=float(data.get('daily_goal', 1)),
            unit=data.get('unit', 'veces'),
            active=True,
        )
        return redirect('progreso')
    return render(request, 'saludya_app/habit_form.html')

def habit_edit(request, habit_id):
    if not request.user.is_authenticated:
        return redirect('index')

    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    if request.method == 'POST':
        data = request.POST
        habit.name = data.get('name')
        habit.habit_type = data.get('habit_type')
        habit.daily_goal = float(data.get('daily_goal', 1))
        habit.unit = data.get('unit', 'veces')
        habit.active = 'active' in data
        habit.save()
        return redirect('progreso')
    return render(request, 'saludya_app/habit_form.html', {'habit': habit})

def habit_delete(request, habit_id):
    if not request.user.is_authenticated:
        return redirect('index')

    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    habit.delete()
    return redirect('progreso')

@csrf_exempt
@require_POST
def habit_entry_create(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'No autenticado'}, status=401)

    payload = json.loads(request.body)
    habit = get_object_or_404(Habit, pk=payload.get('habit_id'), user=request.user)
    entry = HabitEntry.objects.create(
        habit=habit,
        date=datetime.date.fromisoformat(payload.get('date')),
        quantity=float(payload.get('quantity', 0)),
        completed=payload.get('completed', False),
        notes=payload.get('notes', ''),
    )

    if entry.completed:
        points_map = {
            'hidratacion': 10,
            'pausa_activa': 15,
            'medicacion': 20,
        }
        points = points_map.get(habit.habit_type, 5)
        profile = _award_points(request.user, points, f'Cumplió {habit.name}', entry=entry)

        if habit.habit_type == 'hidratacion':
            profile.hydration_streak += 1
        elif habit.habit_type == 'pausa_activa':
            profile.pause_streak += 1
        elif habit.habit_type == 'medicacion':
            profile.medication_streak += 1
        profile.save()

        _unlock_badge(request.user, 'Primer logro', 'Completa tu primer hábito del día', icon='🥇')
        _update_challenges(request.user, habit.habit_type, entry.date)

        return JsonResponse({
            'status': 'ok',
            'message': f'¡Has ganado {points} puntos y desbloqueado progreso!',
            'points_total': profile.points_total,
            'next_badge': profile.points_to_next_level,
        })

    return JsonResponse({'status': 'ok'})

def habit_entry_list(request):
    if not request.user.is_authenticated:
        return JsonResponse({'entries': []})

    entries = HabitEntry.objects.filter(habit__user=request.user).order_by('-date')[:20]
    data = [
        {
            'habit': entry.habit.name,
            'date': entry.date.isoformat(),
            'quantity': entry.quantity,
            'completed': entry.completed,
            'notes': entry.notes,
        }
        for entry in entries
    ]
    return JsonResponse({'entries': data})

def export_progress_pdf(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = _get_profile(request.user)
    habits = Habit.objects.filter(user=request.user, active=True)
    badges = Badge.objects.filter(user=request.user, achieved=True)
    lines = [
        f'Informe SaludYa para {request.user.username}',
        '',
        f'Puntos totales: {profile.points_total}',
        f'Nivel: {profile.level}',
        f'Siguiente insignia en: {profile.points_to_next_level} puntos',
        '',
        f'Hábitos activos: {habits.count()}',
        f'Insignias desbloqueadas: {badges.count()}',
        '',
        'Resumen de recompensas y retos:',
    ]
    for badge in badges:
        lines.append(f'- {badge.name}: {badge.description}')
    line_count = len(lines)
    if line_count < 20:
        lines += [''] * (20 - line_count)
    for habit in habits:
        lines.append(f'- {habit.name}: {habit.daily_goal} {habit.unit}')
    if badges.exists():
        lines.append('')
        lines.append('Insignias:')
        for badge in badges:
            lines.append(f'- {badge.name} ({badge.date_awarded or "Pendiente"})')

    pdf_bytes = _build_simple_pdf(lines)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="saludya-progreso.pdf"'
    return response


def api_gamification(request):
    if not request.user.is_authenticated:
        return JsonResponse({'profile': None})
    profile = _get_profile(request.user)
    return JsonResponse({
        'profile': {
            'points_total': profile.points_total,
            'level': profile.level,
            'next_badge_target': profile.next_badge_target,
            'points_to_next_level': profile.points_to_next_level,
        }
    })


def api_badges(request):
    if not request.user.is_authenticated:
        return JsonResponse({'badges': []})
    badges = Badge.objects.filter(user=request.user)
    return JsonResponse({'badges': [
        {
            'name': badge.name,
            'description': badge.description,
            'icon': badge.icon,
            'condition': badge.condition,
            'achieved': badge.achieved,
            'date_awarded': badge.date_awarded.isoformat() if badge.date_awarded else None,
        }
        for badge in badges
    ]})


def api_rewards(request):
    rewards = Reward.objects.filter(active=True)
    return JsonResponse({'rewards': [
        {
            'id': reward.id,
            'name': reward.name,
            'description': reward.description,
            'icon': reward.icon,
            'cost_points': reward.cost_points,
            'stock': reward.stock,
        }
        for reward in rewards
    ]})


def api_points(request):
    if not request.user.is_authenticated:
        return JsonResponse({'points_total': 0, 'level': 1, 'next_badge_target': 100})
    profile = _get_profile(request.user)
    return JsonResponse({
        'points_total': profile.points_total,
        'level': profile.level,
        'next_badge_target': profile.next_badge_target,
        'points_to_next_level': profile.points_to_next_level,
    })


def api_progress(request):
    if not request.user.is_authenticated:
        return JsonResponse({'progress': []})

    records = ProgressRecord.objects.filter(user=request.user).order_by('-date')[:30]
    data = [
        {
            'date': record.date.isoformat(),
            'period': record.period,
            'hydration_pct': record.hydration_pct,
            'pause_pct': record.pause_pct,
            'medication_pct': record.medication_pct,
        }
        for record in records
    ]
    return JsonResponse({'progress': data})

def api_habits(request):
    if not request.user.is_authenticated:
        return JsonResponse({'habits': []})

    habits = Habit.objects.filter(user=request.user)
    data = [
        {
            'id': habit.id,
            'name': habit.name,
            'type': habit.habit_type,
            'daily_goal': habit.daily_goal,
            'unit': habit.unit,
            'active': habit.active,
        }
        for habit in habits
    ]
    return JsonResponse({'habits': data})


def _get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def _recommend_products(user):
    habit_types = list(Habit.objects.filter(user=user).values_list('habit_type', flat=True))
    if not habit_types:
        return Product.objects.filter(featured=True, stock__gt=0)[:4]

    category_map = {
        'hidratacion': ['hidratacion', 'suplementos'],
        'pausa_activa': ['ejercicio', 'suplementos'],
        'medicacion': ['nutricion', 'suplementos'],
    }
    categories = set()
    for habit_type in habit_types:
        categories.update(category_map.get(habit_type, []))
    recommendations = Product.objects.filter(
        Q(category__name__in=categories) | Q(featured=True),
        stock__gt=0,
    ).distinct().order_by('-popularity')[:8]
    return recommendations


def marketplace(request):
    categories = MarketplaceCategory.objects.filter(active=True)
    products = Product.objects.filter(stock__gt=0)
    featured = Product.objects.filter(featured=True, stock__gt=0)[:6]
    recommended = _recommend_products(request.user) if request.user.is_authenticated else featured

    category_slug = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))

    cart = _get_user_cart(request.user) if request.user.is_authenticated else None
    context = {
        'categories': categories,
        'products': products,
        'featured': featured,
        'recommended': recommended,
        'cart': cart,
    }
    return render(request, 'saludya_app/marketplace.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = ProductReview.objects.filter(product=product)
    cart = _get_user_cart(request.user) if request.user.is_authenticated else None
    return render(request, 'saludya_app/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'cart': cart,
    })


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Debes iniciar sesión para añadir al carrito.'}, status=401)

    product = get_object_or_404(Product, pk=product_id, stock__gt=0)
    cart = _get_user_cart(request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    product.popularity += 1
    product.save()
    return JsonResponse({'status': 'ok', 'quantity': cart_item.quantity, 'cart_total': float(cart.total)})


def remove_from_cart(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Debes iniciar sesión para modificar el carrito.'}, status=401)

    cart = _get_user_cart(request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.delete()
    return JsonResponse({'status': 'ok', 'cart_total': float(cart.total)})


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('index')

    cart = _get_user_cart(request.user)
    return render(request, 'saludya_app/cart.html', {'cart': cart})


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('index')

    cart = _get_user_cart(request.user)
    profile = _get_profile(request.user)
    points_available = profile.points_total
    points_discount = 0

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', '').strip()
        points_redeem = int(request.POST.get('points_redeem', 0) or 0)
        coupon = None

        if coupon_code:
            coupon = Coupon.objects.filter(code__iexact=coupon_code, active=True).first()
            if coupon:
                cart.coupon = coupon
                cart.save()

        if points_redeem > 0 and points_redeem <= points_available:
            subtotal = float(sum(item.product.price * item.quantity for item in cart.items.all()))
            points_discount = min(points_redeem, int(subtotal))
            profile.points_total -= points_discount
            profile.save()
        else:
            points_discount = 0

        if cart.items.count() == 0:
            return redirect('marketplace')

        subtotal = float(sum(item.product.price * item.quantity for item in cart.items.all()))
        total_amount = float(cart.total) - points_discount
        total_amount = max(0.0, total_amount)

        order = Order.objects.create(
            user=request.user,
            coupon=cart.coupon,
            total=total_amount,
            discount_amount=subtotal - total_amount,
            status='completed',
            completed_at=datetime.datetime.now(),
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price,
            )
            item.product.stock = max(0, item.product.stock - item.quantity)
            item.product.save()
        cart.items.all().delete()
        cart.coupon = None
        cart.save()
        return render(request, 'saludya_app/checkout_success.html', {'order': order})

    return render(request, 'saludya_app/checkout.html', {
        'cart': cart,
        'profile': profile,
        'points_available': points_available,
    })


def category_list(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    categories = MarketplaceCategory.objects.all()
    return render(request, 'saludya_app/category_list.html', {'categories': categories})


def category_create(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        slug = request.POST.get('slug', '').strip() or slugify(name)
        description = request.POST.get('description', '').strip()
        active = 'active' in request.POST
        MarketplaceCategory.objects.create(
            name=name,
            slug=slug,
            description=description,
            active=active,
        )
        return redirect('category_list')

    return render(request, 'saludya_app/category_form.html', {'category': None})


def category_edit(request, category_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    category = get_object_or_404(MarketplaceCategory, pk=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name', '').strip()
        category.slug = request.POST.get('slug', '').strip() or slugify(category.name)
        category.description = request.POST.get('description', '').strip()
        category.active = 'active' in request.POST
        category.save()
        return redirect('category_list')

    return render(request, 'saludya_app/category_form.html', {'category': category})


def category_delete(request, category_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    category = get_object_or_404(MarketplaceCategory, pk=category_id)
    category.delete()
    return redirect('category_list')


def product_create(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    categories = MarketplaceCategory.objects.filter(active=True)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '0').strip()
        image_url = request.POST.get('image_url', '').strip()
        stock = int(request.POST.get('stock', '0') or 0)
        featured = 'featured' in request.POST
        category_id = request.POST.get('category')
        category = MarketplaceCategory.objects.filter(pk=category_id).first() if category_id else None
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            stock=stock,
            featured=featured,
            category=category,
        )
        return redirect('marketplace')

    return render(request, 'saludya_app/product_form.html', {'product': None, 'categories': categories})


def product_edit(request, product_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    product = get_object_or_404(Product, pk=product_id)
    categories = MarketplaceCategory.objects.filter(active=True)
    if request.method == 'POST':
        product.name = request.POST.get('name', '').strip()
        product.description = request.POST.get('description', '').strip()
        product.price = request.POST.get('price', '0').strip()
        product.image_url = request.POST.get('image_url', '').strip()
        product.stock = int(request.POST.get('stock', '0') or 0)
        product.featured = 'featured' in request.POST
        category_id = request.POST.get('category')
        product.category = MarketplaceCategory.objects.filter(pk=category_id).first() if category_id else None
        product.save()
        return redirect('product_detail', product_id=product.id)

    return render(request, 'saludya_app/product_form.html', {'product': product, 'categories': categories})


def product_delete(request, product_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('marketplace')


def order_history(request):
    if not request.user.is_authenticated:
        return redirect('index')

    orders = Order.objects.filter(user=request.user)
    return render(request, 'saludya_app/order_history.html', {'orders': orders})


def export_orders_pdf(request):
    if not request.user.is_authenticated:
        return redirect('index')

    orders = Order.objects.filter(user=request.user)
    lines = [f'Historial de pedidos para {request.user.username}', '']
    for order in orders:
        lines.append(f'Pedido {order.id} - {order.created_at.date()} - {order.status} - Total: {order.total}')
        for item in order.items.all():
            lines.append(f'  • {item.product.name if item.product else "Producto eliminado"} x{item.quantity} - {item.price_at_purchase}')
    pdf_bytes = _build_simple_pdf(lines)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="saludya-pedidos.pdf"'
    return response


def api_products(request):
    products = Product.objects.filter(stock__gt=0)
    data = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'image_url': product.image_url,
            'stock': product.stock,
            'category': product.category.name if product.category else None,
        }
        for product in products
    ]
    return JsonResponse({'products': data})


def api_orders(request):
    if not request.user.is_authenticated:
        return JsonResponse({'orders': []})
    orders = Order.objects.filter(user=request.user)
    data = [
        {
            'id': order.id,
            'total': float(order.total),
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'items': [
                {
                    'product': item.product.name if item.product else None,
                    'quantity': item.quantity,
                    'price': float(item.price_at_purchase),
                }
                for item in order.items.all()
            ],
        }
        for order in orders
    ]
    return JsonResponse({'orders': data})

def historial(request):
    return render(request, 'historial.html')
