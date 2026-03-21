from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import F

# --- MODELO ESTUDIANTE ---
# (Asumiendo que así lo tenías estructurado, si tiene más campos, déjalos)
class Estudiante(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

# --- MODELO EQUIPO ---
class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cantidad_total = models.PositiveIntegerField(default=1)
    cantidad_disponible = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nombre

# --- MODELO PRESTAMO ---
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

    # --- LÓGICA AL GUARDAR O ACTUALIZAR ---
    def save(self, *args, **kwargs):
        
        # 1. Bloquear si el estudiante ya tiene un préstamo activo
        if self.estado == 'ACTIVO':
            prestamos_activos = Prestamo.objects.filter(
                estudiante=self.estudiante, 
                estado='ACTIVO'
            ).exclude(pk=self.pk)
            
            if prestamos_activos.exists():
                raise ValidationError(f"¡Bloqueado! El estudiante {self.estudiante.email} ya tiene un equipo sin devolver.")

        # 2. Refrescar los datos del equipo directamente desde la BD
        if getattr(self, 'equipo_id', None):
            self.equipo.refresh_from_db()

        # 3. Escenario A: Es un préstamo NUEVO y está ACTIVO (Resta 1 exacto en BD)
        if not self.pk and self.estado == 'ACTIVO':
            if self.equipo.cantidad_disponible > 0:
                self.equipo.cantidad_disponible = F('cantidad_disponible') - 1
                self.equipo.save(update_fields=['cantidad_disponible'])
            else:
                raise ValidationError(f"¡Ya no hay '{self.equipo.nombre}' disponibles en la bodega!")
        
        # 4. Escenario B: El préstamo ya existía y le están cambiando el estado
        elif self.pk:
            viejo_prestamo = Prestamo.objects.get(pk=self.pk)
            
            # B1: Pasa de ACTIVO a DEVUELTO (Suma 1 exacto en BD)
            if viejo_prestamo.estado == 'ACTIVO' and self.estado == 'DEVUELTO':
                self.equipo.cantidad_disponible = F('cantidad_disponible') + 1
                self.equipo.save(update_fields=['cantidad_disponible'])
                
            # B2: Pasa de DEVUELTO a ACTIVO (Resta 1 exacto en BD)
            elif viejo_prestamo.estado != 'ACTIVO' and self.estado == 'ACTIVO':
                if self.equipo.cantidad_disponible > 0:
                    self.equipo.cantidad_disponible = F('cantidad_disponible') - 1
                    self.equipo.save(update_fields=['cantidad_disponible'])
                else:
                    raise ValidationError(f"¡Ya no hay '{self.equipo.nombre}' para reactivar el préstamo!")

        super().save(*args, **kwargs)

    # --- LÓGICA AL ELIMINAR EL REGISTRO ---
    def delete(self, *args, **kwargs):
        if getattr(self, 'equipo_id', None):
            self.equipo.refresh_from_db()
            
        # Si borran el registro mientras estaba Activo, devolvemos el balón
        if self.estado == 'ACTIVO':
            self.equipo.cantidad_disponible = F('cantidad_disponible') + 1
            self.equipo.save(update_fields=['cantidad_disponible'])
            
        super().delete(*args, **kwargs)