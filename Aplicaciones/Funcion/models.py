from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"





# models.py (Modelo Proyecto)
from django.db import models
from django.utils import timezone

class Proyecto(models.Model):
    ESTADO_CHOICES = [
        ('planificacion', 'Planificación'),
        ('diseno', 'Diseño'),
        ('construccion', 'Construcción'),
        ('terminado', 'Terminado'),
        ('pausado', 'Pausado'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='proyectos')
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    fecha_fin_real = models.DateField(null=True, blank=True)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificacion')
    ubicacion = models.CharField(max_length=255)
    metros_cuadrados = models.IntegerField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.cliente}"
        
    def esta_retrasado(self):
        if not self.fecha_fin_real and self.fecha_fin_estimada < timezone.now().date():
            return True
        return False
        
    def porcentaje_completado(self):
        if self.estado == 'terminado':
            return 100
        elif self.estado == 'planificacion':
            return 10
        elif self.estado == 'diseno':
            return 30
        elif self.estado == 'construccion':
            return 70
        else:
            return 0