from djongo import models
from django.contrib.auth.models import User
import datetime

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    edad = models.IntegerField()
    # Categoría: Estudiante, Trabajador, Adulto Mayor
    tipo_usuario = models.CharField(max_length=50)

class Recordatorio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    hora = models.TimeField()
    repeticion_diaria = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)

class Hidratacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meta_vasos_diarios = models.IntegerField(default=8)
    vasos_tomados = models.IntegerField(default=0)
    fecha = models.DateField(auto_now_add=True)

class Medicacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_medicamento = models.CharField(max_length=100)
    dosis = models.CharField(max_length=100, blank=True)
    fecha_programada = models.DateField(null=True, blank=True)
    hora = models.TimeField()
    tomado = models.BooleanField(default=False)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)

class Actividad(models.Model):
    CATEGORIAS = [
        ('Actividad Física', 'Actividad Física'),
        ('Gimnasio', 'Gimnasio'),
        ('Ciclismo', 'Ciclismo'),
        ('Caminata', 'Caminata'),
        ('Estiramiento', 'Estiramiento'),
        ('Otro', 'Otro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    descripcion = models.CharField(max_length=255, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    minutos_caminando = models.IntegerField(default=0)
    minutos_inactividad = models.IntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['categoria', 'fecha', 'hora']

class PausaActiva(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frecuencia_minutos = models.IntegerField(default=60) # Cada cuánto tiempo avisar
    cumplimiento = models.FloatField(default=0.0) # Porcentaje 0.0 a 1.0


class GamificationProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points_total = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    hydration_streak = models.IntegerField(default=0)
    pause_streak = models.IntegerField(default=0)
    medication_streak = models.IntegerField(default=0)
    next_badge_target = models.IntegerField(default=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Gamification"

    @property
    def points_to_next_level(self):
        return max(0, self.next_badge_target - self.points_total)


class PointTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit_entry = models.ForeignKey('HabitEntry', on_delete=models.SET_NULL, null=True, blank=True)
    points = models.IntegerField(default=0)
    reason = models.CharField(max_length=180)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.user.username} +{self.points} pts ({self.reason})"


class Challenge(models.Model):
    HABIT_TYPES = [
        ('hidratacion', 'Hidratación'),
        ('pausa_activa', 'Pausa Activa'),
        ('medicacion', 'Medicación'),
    ]

    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    habit_type = models.CharField(max_length=20, choices=HABIT_TYPES)
    target_days = models.IntegerField(default=7)
    reward_points = models.IntegerField(default=50)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    days_completed = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'challenge')

    def progress_percent(self):
        return int((self.days_completed / self.challenge.target_days) * 100)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.name}"


class Reward(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='🎁')
    cost_points = models.IntegerField(default=100)
    active = models.BooleanField(default=True)
    stock = models.IntegerField(default=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RewardRedemption(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    points_spent = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.reward.name} ({self.status})"


class Habit(models.Model):
    HABIT_TYPES = [
        ('hidratacion', 'Hidratación'),
        ('pausa_activa', 'Pausa Activa'),
        ('medicacion', 'Medicación'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    habit_type = models.CharField(max_length=20, choices=HABIT_TYPES)
    daily_goal = models.FloatField(default=1.0)
    unit = models.CharField(max_length=30, default='veces')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class HabitEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField()
    quantity = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.habit.name} @ {self.date}"


class ProgressRecord(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    hydration_pct = models.FloatField(default=0.0)
    pause_pct = models.FloatField(default=0.0)
    medication_pct = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.period} {self.date}"


class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=80, default='🏅')
    condition = models.CharField(max_length=180, blank=True)
    achieved = models.BooleanField(default=False)
    date_awarded = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class MarketplaceCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categorías de Marketplace'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(MarketplaceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image_url = models.CharField(max_length=255, blank=True)
    stock = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    popularity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_percent = models.IntegerField(default=10)
    active = models.BooleanField(default=True)
    min_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expires_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.code


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        total = sum(item.product.price * item.quantity for item in self.items.all())
        if self.coupon and self.coupon.active and (self.coupon.min_total <= total) and (not self.coupon.expires_at or self.coupon.expires_at >= datetime.date.today()):
            discount = (total * self.coupon.discount_percent) / 100
            return total - discount
        return total

    def __str__(self):
        return f"Carrito de {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        if self.product:
            return f"{self.quantity} x {self.product.name}"
        return f"{self.quantity} x Producto eliminado"
