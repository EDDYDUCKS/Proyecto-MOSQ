from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudianteViewSet, EquipoViewSet, PrestamoViewSet

# El router crea automáticamente las URLs para el CRUD completo
router = DefaultRouter()
router.register(r'equipos', EquipoViewSet)
router.register(r'estudiantes', EstudianteViewSet)
router.register(r'prestamos', PrestamoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]