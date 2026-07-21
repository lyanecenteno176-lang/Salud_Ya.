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
import logging

logger = logging.getLogger(__name__)


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


# ==================== VISTAS PRINCIPALES ====================

def index(request):
    """Página principal de la aplicación."""
    return render(request, 'saludya_app/Index.html')


def registro(request):
    """Página de registro de usuarios."""
    return render(request, 'saludya_app/registro.html')


def config_agua(request):
    """Configuración de recordatorios de hidratación."""
    return render(request, 'saludya_app/config-agua.html')


def config_ejercicios(request):
    """Configuración de pausas activas."""
    return render(request, 'saludya_app/config-ejercicios.html')


def config_medicinas(request):
    """Configuración de medicamentos."""
    return render(request, 'saludya_app/config-medicinas.html')


def perfil(request):
    """Página de perfil del usuario."""
    return render(request, 'saludya_app/perfil.html')


# ==================== FUNCIONES AUXILIARES ====================

def _get_profile(user):
    """Obtiene o crea el perfil de gamificación del usuario."""
    if not user or not user.is_authenticated:
        return None
    profile, created = GamificationProfile.objects.get_or_create(user=user)
    return profile


def _unlock_badge(user, name, description, icon='🏅'):
    """
    Desbloquea una insignia para el usuario.
    
    Args:
        user: Usuario que obtiene la insignia
        name: Nombre de la insignia
        description: Descripción de la insignia
        icon: Emoji o ícono de la insignia
    """
    if not user or not user.is_authenticated:
        return None
    
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
    """
    Otorga puntos al usuario y verifica si sube de nivel.
    
    Args:
        user: Usuario que recibe los puntos
        amount: Cantidad de puntos a otorgar
        reason: Razón del otorgamiento
        entry: Entrada de hábito relacionada (opcional)
    
    Returns:
        GamificationProfile actualizado
    """
    if not user or not user.is_authenticated:
        return None
    
    profile = _get_profile(user)
    if not profile:
        return None
        
    profile.points_total += amount
    
    # Verificar si sube de nivel
    if profile.points_total >= profile.next_badge_target:
        profile.level += 1
        profile.next_badge_target += 100
        _unlock_badge(user, f'Level {profile.level}', f'Has alcanzado el nivel {profile.level}', icon='🥇')
    
    profile.save()
    
    # Registrar transacción de puntos
    PointTransaction.objects.create(
        user=user,
        habit_entry=entry,
        points=amount,
        reason=reason,
    )
    return profile


def _update_challenges(user, habit_type, date):
    """
    Actualiza el progreso de retos relacionados con un tipo de hábito.
    
    Args:
        user: Usuario que completa el hábito
        habit_type: Tipo de hábito (hidratacion, pausa_activa, medicacion)
        date: Fecha de la actividad
    """
    if not user or not user.is_authenticated:
        return
    
    try:
        active_challenges = UserChallenge.objects.filter(
            user=user, 
            challenge__habit_type=habit_type, 
            completed=False
        )
        
        for user_challenge in active_challenges:
            if user_challenge.last_activity_date == date:
                continue
                
            if user_challenge.last_activity_date == date - datetime.timedelta(days=1):
                user_challenge.days_completed += 1
            else:
                user_challenge.days_completed = 1
            
            user_challenge.last_activity_date = date
            
            # Verificar si el reto está completo
            if user_challenge.days_completed >= user_challenge.challenge.target_days:
                user_challenge.completed = True
                user_challenge.completed_at = date
                _award_points(user, user_challenge.challenge.reward_points, 
                            f'Completó reto {user_challenge.challenge.name}')
                _unlock_badge(user, f'Reto {user_challenge.challenge.name}', 
                            user_challenge.challenge.description, icon='🏆')
            
            user_challenge.save()
    except Exception as e:
        logger.error(f"Error actualizando desafíos para usuario {user.id}: {str(e)}")


# ==================== VISTAS DE PROGRESO Y GAMIFICACIÓN ====================

def progreso(request):
    """Vista del panel de progreso del usuario."""
    if not request.user.is_authenticated:
        return redirect('index')
    
    user = request.user
    habits = Habit.objects.filter(user=user, active=True)
    entries = HabitEntry.objects.filter(habit__user=user).order_by('-date')[:10]
    badges = Badge.objects.filter(user=user, achieved=True)
    progress_records = ProgressRecord.objects.filter(user=user).order_by('-date')[:4]
    profile = _get_profile(user)
    
    # Calcular progreso de insignia
    badge_progress = 0
    if profile and profile.next_badge_target and profile.next_badge_target > 0:
        badge_progress = int((profile.points_total / profile.next_badge_target) * 100)
        badge_progress = min(badge_progress, 100)  # Limitar a 100%
    
    challenges = UserChallenge.objects.filter(user=user, completed=False)
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
    """Vista del panel de gamificación."""
    if not request.user.is_authenticated:
        return redirect('index')

    profile = _get_profile(request.user)
    
    # Calcular progreso de insignia
    badge_progress = 0
    if profile and profile.next_badge_target and profile.next_badge_target > 0:
        badge_progress = int((profile.points_total / profile.next_badge_target) * 100)
        badge_progress = min(badge_progress, 100)
    
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
    """Canjea una recompensa por puntos."""
    if not request.user.is_authenticated:
        return redirect('index')

    try:
        reward = get_object_or_404(Reward, pk=reward_id, active=True)
        profile = _get_profile(request.user)
        
        # VALIDACIÓN: Verificar que el usuario tenga suficientes puntos y stock disponible
        if not profile:
            return JsonResponse({
                'status': 'error',
                'message': 'No se pudo obtener tu perfil.'
            }, status=400)
        
        if profile.points_total < reward.cost_points:
            return JsonResponse({
                'status': 'error',
                'message': f'Puntos insuficientes. Necesitas {reward.cost_points} pts, tienes {profile.points_total} pts.'
            }, status=400)
        
        if reward.stock <= 0:
            return JsonResponse({
                'status': 'error',
                'message': 'La recompensa está agotada.'
            }, status=400)

        # Procesar el canje
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

        logger.info(f"Usuario {request.user.id} canjeó recompensa {reward.id}")

        return JsonResponse({
            'status': 'ok',
            'message': f'¡Recompensa "{reward.name}" canjeada con éxito!',
            'points_total': profile.points_total,
        })
        
    except Exception as e:
        logger.error(f"Error canjeando recompensa: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Error al procesar el canje.'
        }, status=500)


# ==================== VISTAS DE HÁBITOS ====================

def habit_create(request):
    """Crear un nuevo hábito."""
    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        try:
            data = request.POST
            name = data.get('name', '').strip()
            habit_type = data.get('habit_type', '').strip()
            
            if not name or not habit_type:
                return render(request, 'saludya_app/habit_form.html', 
                            {'error': 'Nombre y tipo de hábito son requeridos.'})
            
            Habit.objects.create(
                user=request.user,
                name=name,
                habit_type=habit_type,
                daily_goal=float(data.get('daily_goal', 1)),
                unit=data.get('unit', 'veces'),
                active=True,
            )
            return redirect('progreso')
        except Exception as e:
            logger.error(f"Error creando hábito: {str(e)}")
            return render(request, 'saludya_app/habit_form.html', 
                        {'error': 'Error al crear el hábito.'})
    
    return render(request, 'saludya_app/habit_form.html')


def habit_edit(request, habit_id):
    """Editar un hábito existente."""
    if not request.user.is_authenticated:
        return redirect('index')

    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    
    if request.method == 'POST':
        try:
            data = request.POST
            habit.name = data.get('name', '').strip()
            habit.habit_type = data.get('habit_type', '').strip()
            habit.daily_goal = float(data.get('daily_goal', 1))
            habit.unit = data.get('unit', 'veces')
            habit.active = 'active' in data
            habit.save()
            return redirect('progreso')
        except Exception as e:
            logger.error(f"Error editando hábito: {str(e)}")
            return render(request, 'saludya_app/habit_form.html', 
                        {'habit': habit, 'error': 'Error al actualizar el hábito.'})
    
    return render(request, 'saludya_app/habit_form.html', {'habit': habit})


def habit_delete(request, habit_id):
    """Eliminar un hábito."""
    if not request.user.is_authenticated:
        return redirect('index')

    habit = get_object_or_404(Habit, pk=habit_id, user=request.user)
    habit.delete()
    logger.info(f"Usuario {request.user.id} eliminó hábito {habit_id}")
    return redirect('progreso')


@csrf_exempt
@require_POST
def habit_entry_create(request):
    """Crear una entrada de hábito (completar un hábito)."""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'No autenticado'}, status=401)

    try:
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

            if profile:
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

        return JsonResponse({'status': 'ok', 'message': 'Entrada registrada.'})
        
    except Exception as e:
        logger.error(f"Error creando entrada de hábito: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error al registrar la entrada.'}, status=400)


def habit_entry_list(request):
    """Obtener lista de entradas de hábitos del usuario."""
    if not request.user.is_authenticated:
        return JsonResponse({'entries': []})

    try:
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
    except Exception as e:
        logger.error(f"Error listando entradas de hábitos: {str(e)}")
        return JsonResponse({'entries': [], 'error': 'Error al obtener historial.'}, status=500)


def export_progress_pdf(request):
    """Exportar progreso del usuario a PDF."""
    if not request.user.is_authenticated:
        return redirect('index')

    try:
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
            'Insignias desbloqueadas:',
        ]
        
        for badge in badges:
            lines.append(f'- {badge.name}: {badge.description}')
        
        line_count = len(lines)
        if line_count < 20:
            lines += [''] * (20 - line_count)
        
        lines.append('')
        lines.append('Hábitos activos:')
        for habit in habits:
            lines.append(f'- {habit.name}: {habit.daily_goal} {habit.unit}')

        pdf_bytes = _build_simple_pdf(lines)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="saludya-progreso.pdf"'
        return response
    except Exception as e:
        logger.error(f"Error exportando PDF: {str(e)}")
        return redirect('progreso')


# ==================== APIs ====================

def api_gamification(request):
    """API: Obtener datos de gamificación del usuario."""
    if not request.user.is_authenticated:
        return JsonResponse({'profile': None}, status=401)
    
    try:
        profile = _get_profile(request.user)
        if not profile:
            return JsonResponse({'profile': None}, status=400)
        
        return JsonResponse({
            'profile': {
                'points_total': profile.points_total,
                'level': profile.level,
                'next_badge_target': profile.next_badge_target,
                'points_to_next_level': profile.points_to_next_level,
            }
        })
    except Exception as e:
        logger.error(f"Error en api_gamification: {str(e)}")
        return JsonResponse({'error': 'Error al obtener datos.'}, status=500)


def api_badges(request):
    """API: Obtener insignias del usuario."""
    if not request.user.is_authenticated:
        return JsonResponse({'badges': []}, status=401)
    
    try:
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
    except Exception as e:
        logger.error(f"Error en api_badges: {str(e)}")
        return JsonResponse({'badges': [], 'error': 'Error al obtener insignias.'}, status=500)


def api_rewards(request):
    """API: Obtener recompensas disponibles."""
    try:
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
    except Exception as e:
        logger.error(f"Error en api_rewards: {str(e)}")
        return JsonResponse({'rewards': [], 'error': 'Error al obtener recompensas.'}, status=500)


def api_points(request):
    """API: Obtener puntos del usuario."""
    if not request.user.is_authenticated:
        return JsonResponse({'points_total': 0, 'level': 1, 'next_badge_target': 100}, status=401)
    
    try:
        profile = _get_profile(request.user)
        if not profile:
            return JsonResponse({'points_total': 0, 'level': 1, 'next_badge_target': 100})
        
        return JsonResponse({
            'points_total': profile.points_total,
            'level': profile.level,
            'next_badge_target': profile.next_badge_target,
            'points_to_next_level': profile.points_to_next_level,
        })
    except Exception as e:
        logger.error(f"Error en api_points: {str(e)}")
        return JsonResponse({'error': 'Error al obtener puntos.'}, status=500)


def api_progress(request):
    """API: Obtener historial de progreso del usuario."""
    if not request.user.is_authenticated:
        return JsonResponse({'progress': []}, status=401)

    try:
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
    except Exception as e:
        logger.error(f"Error en api_progress: {str(e)}")
        return JsonResponse({'progress': [], 'error': 'Error al obtener progreso.'}, status=500)


def api_habits(request):
    """API: Obtener hábitos del usuario."""
    if not request.user.is_authenticated:
        return JsonResponse({'habits': []}, status=401)

    try:
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
    except Exception as e:
        logger.error(f"Error en api_habits: {str(e)}")
        return JsonResponse({'habits': [], 'error': 'Error al obtener hábitos.'}, status=500)


# ==================== VISTAS DEL MARKETPLACE ====================

def _get_user_cart(user):
    """Obtiene o crea el carrito del usuario."""
    if not user or not user.is_authenticated:
        return None
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def _recommend_products(user):
    """Recomienda productos basado en los hábitos del usuario."""
    if not user or not user.is_authenticated:
        return Product.objects.filter(featured=True, stock__gt=0)[:4]
    
    try:
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
    except Exception as e:
        logger.error(f"Error recomendando productos: {str(e)}")
        return Product.objects.filter(featured=True, stock__gt=0)[:4]


def marketplace(request):
    """Vista del marketplace."""
    try:
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
    except Exception as e:
        logger.error(f"Error en marketplace: {str(e)}")
        return render(request, 'saludya_app/marketplace.html', {'error': 'Error al cargar el marketplace.'})


def product_detail(request, product_id):
    """Detalle de un producto."""
    try:
        product = get_object_or_404(Product, pk=product_id)
        reviews = ProductReview.objects.filter(product=product)
        cart = _get_user_cart(request.user) if request.user.is_authenticated else None
        return render(request, 'saludya_app/product_detail.html', {
            'product': product,
            'reviews': reviews,
            'cart': cart,
        })
    except Exception as e:
        logger.error(f"Error en product_detail: {str(e)}")
        return redirect('marketplace')


def add_to_cart(request, product_id):
    """Agregar producto al carrito."""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Debes iniciar sesión para añadir al carrito.'}, status=401)

    try:
        product = get_object_or_404(Product, pk=product_id, stock__gt=0)
        cart = _get_user_cart(request.user)
        
        if not cart:
            return JsonResponse({'status': 'error', 'message': 'Error al acceder al carrito.'}, status=400)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        
        product.popularity += 1
        product.save()
        
        return JsonResponse({'status': 'ok', 'quantity': cart_item.quantity, 'cart_total': float(cart.total)})
    except Exception as e:
        logger.error(f"Error añadiendo al carrito: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error al añadir al carrito.'}, status=500)


def remove_from_cart(request, product_id):
    """Remover producto del carrito."""
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Debes iniciar sesión para modificar el carrito.'}, status=401)

    try:
        cart = _get_user_cart(request.user)
        if not cart:
            return JsonResponse({'status': 'error', 'message': 'Error al acceder al carrito.'}, status=400)
        
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.delete()
        return JsonResponse({'status': 'ok', 'cart_total': float(cart.total)})
    except Exception as e:
        logger.error(f"Error removiendo del carrito: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error al remover del carrito.'}, status=500)


def cart_view(request):
    """Vista del carrito."""
    if not request.user.is_authenticated:
        return redirect('index')

    try:
        cart = _get_user_cart(request.user)
        return render(request, 'saludya_app/cart.html', {'cart': cart})
    except Exception as e:
        logger.error(f"Error en cart_view: {str(e)}")
        return redirect('marketplace')


def checkout(request):
    """Proceso de checkout y creación de orden."""
    if not request.user.is_authenticated:
        return redirect('index')

    try:
        cart = _get_user_cart(request.user)
        profile = _get_profile(request.user)
        points_available = profile.points_total if profile else 0
        points_discount = 0

        if request.method == 'POST':
            # VALIDACIÓN: Verificar que el carrito no esté vacío
            if cart.items.count() == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El carrito está vacío.'
                }, status=400)
            
            coupon_code = request.POST.get('coupon_code', '').strip()
            points_redeem = int(request.POST.get('points_redeem', 0) or 0)
            coupon = None

            # Aplicar cupón si existe
            if coupon_code:
                coupon = Coupon.objects.filter(code__iexact=coupon_code, active=True).first()
                if coupon:
                    cart.coupon = coupon
                    cart.save()
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'El cupón no es válido.'
                    }, status=400)

            # VALIDACIÓN: Verificar puntos para descuento
            if points_redeem > 0:
                if not profile:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Error al obtener tu perfil.'
                    }, status=400)
                
                if points_redeem > points_available:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Puntos insuficientes. Tienes {points_available} pts, solicitaste usar {points_redeem} pts.'
                    }, status=400)
                
                subtotal = float(sum(item.product.price * item.quantity for item in cart.items.all()))
                points_discount = min(points_redeem, int(subtotal))
                profile.points_total -= points_discount
                profile.save()

            # Calcular total
            subtotal = float(sum(item.product.price * item.quantity for item in cart.items.all()))
            total_amount = float(subtotal) - points_discount
            total_amount = max(0.0, total_amount)

            # Crear orden
            order = Order.objects.create(
                user=request.user,
                coupon=cart.coupon,
                total=total_amount,
                discount_amount=subtotal - total_amount,
                status='completed',
                completed_at=datetime.datetime.now(),
            )
            
            # Crear items de la orden y actualizar stock
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.price,
                )
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()
            
            # Limpiar carrito
            cart.items.all().delete()
            cart.coupon = None
            cart.save()
            
            logger.info(f"Usuario {request.user.id} completó orden {order.id}")
            return render(request, 'saludya_app/checkout_success.html', {'order': order})

        return render(request, 'saludya_app/checkout.html', {
            'cart': cart,
            'profile': profile,
            'points_available': points_available,
        })
    except Exception as e:
        logger.error(f"Error en checkout: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error procesando el checkout.'}, status=500)


# ==================== VISTAS DE CATEGORÍAS ====================

def category_list(request):
    """Listar categorías (solo staff)."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    try:
        categories = MarketplaceCategory.objects.all()
        return render(request, 'saludya_app/category_list.html', {'categories': categories})
    except Exception as e:
        logger.error(f"Error listando categorías: {str(e)}")
        return redirect('marketplace')


def category_create(request):
    """Crear categoría (solo staff)."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            slug = request.POST.get('slug', '').strip() or slugify(name)
            description = request.POST.get('description', '').strip()
            active = 'active' in request.POST
            
            if not name:
                return render(request, 'saludya_app/category_form.html', 
                            {'error': 'El nombre es requerido.'})
            
            MarketplaceCategory.objects.create(
                name=name,
                slug=slug,
                description=description,
                active=active,
            )
            return redirect('category_list')
        except Exception as e:
            logger.error(f"Error creando categoría: {str(e)}")
            return render(request, 'saludya_app/category_form.html', 
                        {'error': 'Error al crear la categoría.'})

    return render(request, 'saludya_app/category_form.html', {'category': None})


def category_edit(request, category_id):
    """Editar categoría (solo staff)."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    category = get_object_or_404(MarketplaceCategory, pk=category_id)
    
    if request.method == 'POST':
        try:
            category.name = request.POST.get('name', '').strip()
            category.slug = request.POST.get('slug', '').strip() or slugify(category.name)
            category.description = request.POST.get('description', '').strip()
            category.active = 'active' in request.POST
            category.save()
            return redirect('category_list')
        except Exception as e:
            logger.error(f"Error editando categoría: {str(e)}")
            return render(request, 'saludya_app/category_form.html', 
                        {'category': category, 'error': 'Error al actualizar la categoría.'})

    return render(request, 'saludya_app/category_form.html', {'category': category})


def category_delete(request, category_id):
    """Eliminar categoría (solo staff)."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    category = get_object_or_404(MarketplaceCategory, pk=category_id)
    category.delete()
    logger.info(f"Usuario {request.user.id} eliminó categoría {category_id}")
    return redirect('category_list')


# ==================== VISTAS DE PRODUCTOS ====================

def product_create(request):
    """Crear producto (solo staff)."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    categories = MarketplaceCategory.objects.filter(active=True)
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            price = request.POST.get('price', '0').strip()
            image_url = request.POST.get('image_url', '').strip()
            stock = int(request.POST.get('stock', '0') or 0)
            featured = 'featured' in request.POST
            category_id = request.POST.get('category')
            
            if not name or not price:
                return render(request, 'saludya_app/product_form.html', 
                            {'error': 'Nombre y precio son requeridos.', 'categories': categories})
            
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
        except Exception as e:
            logger.error(f"Error creando producto: {str(e)}")
            return render(request, 'saludya_app/product_form.html', 
                        {'error': 'Error al crear el producto.', 'categories': categories})

    return render(request, 'saludya_app/product_form.html', {'product': None, 'categories': categories})


def product_edit(request, product_id):
    """Editar producto (solo staff)."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    product = get_object_or_404(Product, pk=product_id)
    categories = MarketplaceCategory.objects.filter(active=True)
    
    if request.method == 'POST':
        try:
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
        except Exception as e:
            logger.error(f"Error editando producto: {str(e)}")
            return render(request, 'saludya_app/product_form.html', 
                        {'product': product, 'error': 'Error al actualizar el producto.', 'categories': categories})

    return render(request, 'saludya_app/product_form.html', {'product': product, 'categories': categories})


def product_delete(request, product_id):
    """Eliminar producto (solo staff)."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('marketplace')

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    logger.info(f"Usuario {request.user.id} eliminó producto {product_id}")
    return redirect('marketplace')


# ==================== VISTAS DE ÓRDENES ====================

def order_history(request):
    """Historial de órdenes del usuario."""
    if not request.user.is_authenticated:
        return redirect('index')

    try:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'saludya_app/order_history.html', {'orders': orders})
    except Exception as e:
        logger.error(f"Error en order_history: {str(e)}")
        return redirect('marketplace')


def export_orders_pdf(request):
    """Exportar historial de órdenes a PDF."""
    if not request.user.is_authenticated:
        return redirect('index')

    try:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        lines = [f'Historial de pedidos para {request.user.username}', '']
        
        for order in orders:
            lines.append(f'Pedido {order.id} - {order.created_at.date()} - {order.status} - Total: ${order.total}')
            for item in order.items.all():
                product_name = item.product.name if item.product else "Producto eliminado"
                lines.append(f'  • {product_name} x{item.quantity} - ${item.price_at_purchase}')
            lines.append('')
        
        pdf_bytes = _build_simple_pdf(lines)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="saludya-pedidos.pdf"'
        return response
    except Exception as e:
        logger.error(f"Error exportando órdenes PDF: {str(e)}")
        return redirect('order_history')


# ==================== APIs DEL MARKETPLACE ====================

def api_products(request):
    """API: Obtener productos disponibles."""
    try:
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
    except Exception as e:
        logger.error(f"Error en api_products: {str(e)}")
        return JsonResponse({'products': [], 'error': 'Error al obtener productos.'}, status=500)


def api_orders(request):
    """API: Obtener órdenes del usuario."""
    if not request.user.is_authenticated:
        return JsonResponse({'orders': []}, status=401)
    
    try:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
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
    except Exception as e:
        logger.error(f"Error en api_orders: {str(e)}")
        return JsonResponse({'orders': [], 'error': 'Error al obtener órdenes.'}, status=500)
