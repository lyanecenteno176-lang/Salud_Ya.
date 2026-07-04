from djongo import models
from django.contrib.auth.models import User

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
    hora = models.TimeField()
    tomado = models.BooleanField(default=False)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)

class PausaActiva(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frecuencia_minutos = models.IntegerField(default=60) # Cada cuánto tiempo avisar
    cumplimiento = models.FloatField(default=0.0) # Porcentaje 0.0 a 1.0