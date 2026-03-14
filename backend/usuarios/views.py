from rest_framework import viewsets
from .models import Estudiante, Equipo, Prestamo
from .serializers import EstudianteSerializer, EquipoSerializer, PrestamoSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all() # Busca todos los equipos
    serializer_class = EquipoSerializer # Usa el traductor de equipos

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer