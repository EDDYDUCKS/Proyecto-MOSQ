from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models

class Estudiante(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cantidad_total = models.PositiveIntegerField(default=1)
    cantidad_disponible = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nombre


class Prestamo(models.Model):
    ESTADOS_PRESTAMO = [
        ('ACTIVO', 'Activo'),
        ('DEVUELTO', 'Devuelto'),
        ('ATRASADO', 'Atrasado'),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PRESTAMO, default='ACTIVO')

    def __str__(self):
        return f"{self.equipo.nombre} prestado a {self.estudiante.email}"

    # --- 1. LÓGICA AL GUARDAR O ACTUALIZAR ---
    def save(self, *args, **kwargs):
        # Escenario A: Es un préstamo NUEVO y está ACTIVO (Resta 1)
        if not self.pk and self.estado == 'ACTIVO':
            if self.equipo.cantidad_disponible > 0:
                self.equipo.cantidad_disponible -= 1
                self.equipo.save()
            else:
                raise ValidationError(f"¡Ya no hay '{self.equipo.nombre}' disponibles en la bodega!")
        
        # Escenario B: El préstamo ya existía y lo están cambiando a DEVUELTO (Suma 1)
        elif self.pk:
            viejo_prestamo = Prestamo.objects.get(pk=self.pk)
            if viejo_prestamo.estado == 'ACTIVO' and self.estado == 'DEVUELTO':
                self.equipo.cantidad_disponible += 1
                self.equipo.save()

        super().save(*args, **kwargs)

    # --- 2. LÓGICA AL ELIMINAR EL REGISTRO ---
    def delete(self, *args, **kwargs):
        # Si deciden borrar el registro de la base de datos mientras estaba Activo (Suma 1)
        if self.estado == 'ACTIVO':
            self.equipo.cantidad_disponible += 1
            self.equipo.save()
            
        super().delete(*args, **kwargs)