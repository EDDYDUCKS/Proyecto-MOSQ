from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import F
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# --- MODELO ESTUDIANTE ---
class Estudiante(AbstractUser):
    CARRERAS_ULSA = [
        ('LAF', 'Licenciatura Administrativa con Énfasis en Finanzas'),
        ('LCM', 'Licenciatura Comercial con Énfasis en Mercadeo'),
        ('IGI', 'Ingeniería en Gestión Industrial'),
        ('ICE', 'Ingeniería Cibernética Electrónica'),
        ('IME', 'Ingeniería Mecánica y Energías Renovables'),
        ('IMS', 'Ingeniería Mecatrónica y Sistemas de Control'),
        ('IEM', 'Ingeniería Electromédica'),
    ]
    carnet = models.CharField(max_length=20, null=True, blank=True)
    carrera = models.CharField(max_length=5, choices=CARRERAS_ULSA, null=True, blank=True)
    ano_cursado = models.CharField(max_length=20, null=True, blank=True)
    sancionado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

# --- MODELO EQUIPO ---
class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    # Aquí puedes agregar la imagen después si lo deciden: imagen = models.URLField(blank=True, null=True)
    cantidad_total = models.PositiveIntegerField(default=1)
    cantidad_disponible = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nombre

# --- MODELO PRESTAMO (EL TICKET GENERAL) ---
class Prestamo(models.Model):
    ESTADOS_PRESTAMO = [
        ('ACTIVO', 'Activo'),
        ('DEVUELTO', 'Devuelto'),
        ('ATRASADO', 'Atrasado'),
    ]
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prestamos_recibidos')
    entregado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='prestamos_entregados')
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PRESTAMO, default='ACTIVO')

    def __str__(self):
        return f"Ticket #{self.id} - {self.estudiante.username}"

    def save(self, *args, **kwargs):
        # 1. Bloqueos de Seguridad
        if self.estado == 'ACTIVO':
            if self.estudiante.sancionado:
                raise ValidationError(f"¡Bloqueado! {self.estudiante.username} está sancionado.")
            if not self.estudiante.carnet or not self.estudiante.carrera:
                raise ValidationError("¡Perfil incompleto! Se requiere carnet y carrera.")
            
            # Solo permitimos 1 ticket activo a la vez por estudiante
            prestamos_activos = Prestamo.objects.filter(
                estudiante=self.estudiante, estado='ACTIVO'
            ).exclude(pk=self.pk)
            if prestamos_activos.exists():
                raise ValidationError(f"¡Bloqueado! {self.estudiante.username} ya tiene un carrito sin devolver.")

        # 2. Devolución automática al inventario cuando todo el ticket cambia a DEVUELTO
        if self.pk:
            viejo_prestamo = Prestamo.objects.get(pk=self.pk)
            if viejo_prestamo.estado == 'ACTIVO' and self.estado == 'DEVUELTO':
                for detalle in self.detalles.all():
                    detalle.equipo.refresh_from_db()
                    detalle.equipo.cantidad_disponible = F('cantidad_disponible') + detalle.cantidad
                    detalle.equipo.save(update_fields=['cantidad_disponible'])
            
            # Reactivar un ticket devuelto (resta otra vez)
            elif viejo_prestamo.estado != 'ACTIVO' and self.estado == 'ACTIVO':
                for detalle in self.detalles.all():
                    detalle.equipo.refresh_from_db()
                    if detalle.equipo.cantidad_disponible >= detalle.cantidad:
                        detalle.equipo.cantidad_disponible = F('cantidad_disponible') - detalle.cantidad
                        detalle.equipo.save(update_fields=['cantidad_disponible'])
                    else:
                        raise ValidationError(f"¡Faltan '{detalle.equipo.nombre}' en bodega para reactivar!")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Si borramos el ticket entero, regresamos todo a la bodega
        if self.estado == 'ACTIVO':
            for detalle in self.detalles.all():
                detalle.equipo.refresh_from_db()
                detalle.equipo.cantidad_disponible = F('cantidad_disponible') + detalle.cantidad
                detalle.equipo.save(update_fields=['cantidad_disponible'])
        super().delete(*args, **kwargs)

# --- NUEVO: MODELO DETALLE_PRESTAMO (LAS LÍNEAS DEL CARRITO) ---
class DetallePrestamo(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='detalles')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.equipo.nombre}"

    def save(self, *args, **kwargs):
        # Cuando se agrega un equipo al carrito, se resta de la bodega
        if not self.pk and self.prestamo.estado == 'ACTIVO':
            self.equipo.refresh_from_db()
            if self.equipo.cantidad_disponible >= self.cantidad:
                self.equipo.cantidad_disponible = F('cantidad_disponible') - self.cantidad
                self.equipo.save(update_fields=['cantidad_disponible'])
            else:
                raise ValidationError(f"¡Solo hay {self.equipo.cantidad_disponible} '{self.equipo.nombre}' disponibles!")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Si quitan un equipo del carrito, lo devolvemos a la bodega
        if self.prestamo.estado == 'ACTIVO':
            self.equipo.refresh_from_db()
            self.equipo.cantidad_disponible = F('cantidad_disponible') + self.cantidad
            self.equipo.save(update_fields=['cantidad_disponible'])
        super().delete(*args, **kwargs)