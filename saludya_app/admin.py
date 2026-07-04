from django.contrib import admin
from .models import PerfilUsuario, Recordatorio, Hidratacion, Medicacion, PausaActiva

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
    list_display = ('user', 'nombre_medicamento', 'hora', 'tomado')
    list_filter = ('tomado',)

@admin.register(PausaActiva)
class PausaActivaAdmin(admin.ModelAdmin):
    list_display = ('user', 'frecuencia_minutos', 'cumplimiento')