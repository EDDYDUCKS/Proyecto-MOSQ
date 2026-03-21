from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import F
from django.contrib.auth.models import AbstractUser # <--- ¡El salvavidas!
from django.conf import settings

# --- MODELO ESTUDIANTE (Con superpoderes de Login y Menú de Carreras) ---
class Estudiante(AbstractUser):
    
    # NUEVO: El menú estricto de carreras de la ULSA
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
    # Le agregamos el choices y bajamos el max_length porque en la BD solo guardaremos las siglas (ej: 'ICE')
    carrera = models.CharField(max_length=5, choices=CARRERAS_ULSA, null=True, blank=True)
    ano_cursado = models.CharField(max_length=20, null=True, blank=True)
    
    sancionado = models.BooleanField(default=False)

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

    # La persona que recibe (El estudiante)
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prestamos_recibidos')
    
    # El equipo prestado
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    
    # La persona que entrega (El Administrador)
    entregado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='prestamos_entregados')
    
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PRESTAMO, default='ACTIVO')

    def __str__(self):
        return f"{self.equipo.nombre} prestado a {self.estudiante.username}"

    # --- LÓGICA AL GUARDAR O ACTUALIZAR ---
    def save(self, *args, **kwargs):
        
        # --- CANDADOS DE REGLAS DE NEGOCIO ---
        if self.estado == 'ACTIVO':
            if self.estudiante.sancionado:
                raise ValidationError(f"¡Bloqueado! El estudiante {self.estudiante.username} está sancionado. Debe ir a Bienestar Estudiantil.")
            
            if not self.estudiante.carnet or not self.estudiante.carrera:
                raise ValidationError("¡Perfil incompleto! El estudiante debe actualizar su carnet y carrera para su primer préstamo.")

            prestamos_activos = Prestamo.objects.filter(
                estudiante=self.estudiante, 
                estado='ACTIVO'
            ).exclude(pk=self.pk)
            
            if prestamos_activos.exists():
                raise ValidationError(f"¡Bloqueado! {self.estudiante.username} ya tiene un equipo sin devolver.")

        # --- LÓGICA DE INVENTARIO ---
        if getattr(self, 'equipo_id', None):
            self.equipo.refresh_from_db()

        if not self.pk and self.estado == 'ACTIVO':
            if self.equipo.cantidad_disponible > 0:
                self.equipo.cantidad_disponible = F('cantidad_disponible') - 1
                self.equipo.save(update_fields=['cantidad_disponible'])
            else:
                raise ValidationError(f"¡Ya no hay '{self.equipo.nombre}' disponibles en la bodega!")
        
        elif self.pk:
            viejo_prestamo = Prestamo.objects.get(pk=self.pk)
            
            if viejo_prestamo.estado == 'ACTIVO' and self.estado == 'DEVUELTO':
                self.equipo.cantidad_disponible = F('cantidad_disponible') + 1
                self.equipo.save(update_fields=['cantidad_disponible'])
                
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
            
        if self.estado == 'ACTIVO':
            self.equipo.cantidad_disponible = F('cantidad_disponible') + 1
            self.equipo.save(update_fields=['cantidad_disponible'])
            
        super().delete(*args, **kwargs)