from django.contrib import admin
from .models import (
    PerfilUsuario,
    Recordatorio,
    Hidratacion,
    Medicacion,
    PausaActiva,
    Actividad,
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

# Registramos los modelos para que aparezcan en el panel de administración
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'edad', 'tipo_usuario')

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('user', 'titulo', 'hora', 'activo')
    list_filter = ('activo',)

@admin.register(Hidratacion)
class HidratacionAdmin(admin.ModelAdmin):
    list_display = ('user', 'vasos_tomados', 'meta_vasos_diarios', 'fecha')

@admin.register(Medicacion)
class MedicacionAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre_medicamento', 'dosis', 'fecha_programada', 'hora', 'tomado')
    list_filter = ('tomado',)

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('user', 'categoria', 'fecha', 'hora', 'minutos_caminando', 'minutos_inactividad')
    list_filter = ('categoria', 'fecha')

@admin.register(PausaActiva)
class PausaActivaAdmin(admin.ModelAdmin):
    list_display = ('user', 'frecuencia_minutos', 'cumplimiento')

@admin.register(MarketplaceCategory)
class MarketplaceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('active',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'featured', 'popularity')
    list_filter = ('category', 'featured', 'stock')
    search_fields = ('name', 'description')

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'active', 'min_total', 'expires_at')
    list_filter = ('active',)
    search_fields = ('code',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'added_at')
    search_fields = ('product__name', 'cart__user__username')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_purchase')
    search_fields = ('product__name', 'order__user__username')
