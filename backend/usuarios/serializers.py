from rest_framework import serializers
from .models import Estudiante, Equipo, Prestamo

# --- TRADUCTOR DE ESTUDIANTES ---
class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        # Agregamos los cajones nuevos para que el Frontend los pueda ver y llenar
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'carnet', 'carrera', 'ano_cursado', 'sancionado']

    # --- EL CADENERO DE CORREOS ---
    def validate_email(self, value):
        # La lista oficial de la ULSA que me acabas de confirmar
        dominios_permitidos = ['@ulsa.edu.ni', '@est.ulsa.edu.ni', '@ac.ulsa.edu.ni']
        
        # Revisamos si el correo que intentan registrar termina en alguno de esos 3
        if not any(value.endswith(dominio) for dominio in dominios_permitidos):
            raise serializers.ValidationError("Acceso denegado. Solo se permiten correos institucionales de la ULSA.")
        
        return value

# --- TRADUCTOR DE EQUIPOS ---
class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

# --- TRADUCTOR DE PRESTAMOS ---
class PrestamoSerializer(serializers.ModelSerializer):
    # Esto es un regalo para Christoffer: le mandamos el detalle completo del estudiante y del equipo,
    # no solo los números de ID, para que le sea más fácil dibujar la página web.
    estudiante_detalle = EstudianteSerializer(source='estudiante', read_only=True)
    equipo_detalle = EquipoSerializer(source='equipo', read_only=True)

    class Meta:
        model = Prestamo
        fields = ['id', 'estudiante', 'estudiante_detalle', 'equipo', 'equipo_detalle', 'entregado_por', 'fecha_prestamo', 'fecha_devolucion', 'estado']