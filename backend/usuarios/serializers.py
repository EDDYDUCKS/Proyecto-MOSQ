from rest_framework import serializers
from .models import Estudiante, Equipo, Prestamo, DetallePrestamo

# --- TRADUCTOR DE ESTUDIANTES ---
class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'carnet', 'carrera', 'ano_cursado', 'sancionado']

    def validate_email(self, value):
        dominios_permitidos = ['@ulsa.edu.ni', '@est.ulsa.edu.ni', '@ac.ulsa.edu.ni']
        if not any(value.endswith(dominio) for dominio in dominios_permitidos):
            raise serializers.ValidationError("Acceso denegado. Solo se permiten correos institucionales de la ULSA.")
        return value

# --- TRADUCTOR DE EQUIPOS ---
class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

# --- TRADUCTOR DE LOS DETALLES DEL CARRITO ---
class DetallePrestamoSerializer(serializers.ModelSerializer):
    equipo_detalle = EquipoSerializer(source='equipo', read_only=True)
    
    class Meta:
        model = DetallePrestamo
        fields = ['id', 'equipo', 'equipo_detalle', 'cantidad']

# --- TRADUCTOR DEL TICKET PRINCIPAL (PRESTAMO) ---
class PrestamoSerializer(serializers.ModelSerializer):
    estudiante_detalle = EstudianteSerializer(source='estudiante', read_only=True)
    # Aquí le decimos que este ticket contiene muchos "detalles" (el carrito)
    detalles = DetallePrestamoSerializer(many=True)

    class Meta:
        model = Prestamo
        fields = ['id', 'estudiante', 'estudiante_detalle', 'entregado_por', 'fecha_prestamo', 'fecha_devolucion', 'estado', 'detalles']

    # MAGIA: Le enseñamos a Django cómo desarmar el paquete JSON de Christoffer y guardarlo en las 2 tablas
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        prestamo = Prestamo.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            DetallePrestamo.objects.create(prestamo=prestamo, **detalle_data)
            
        return prestamo