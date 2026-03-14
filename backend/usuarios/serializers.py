from rest_framework import serializers
from .models import Estudiante, Equipo, Prestamo

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__' # Traduce todas las columnas del balón/equipo

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        # Por seguridad, no enviamos la contraseña, solo datos públicos
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = '__all__'