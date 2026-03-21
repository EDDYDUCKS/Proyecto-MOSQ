from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. El enrutador automático para tu CRUD (Crear, Leer, Actualizar, Borrar)
router = DefaultRouter()
router.register(r'estudiantes', views.EstudianteViewSet)
router.register(r'equipos', views.EquipoViewSet)
router.register(r'prestamos', views.PrestamoViewSet)

# 2. Las URLs finales que exponemos al mundo
urlpatterns = [
    # Incluimos todas las rutas automáticas (ej. /api/equipos/)
    path('', include(router.urls)),
    
    # NUEVA RUTA: El enlace directo para descargar el Excel
    path('reportes/excel/', views.exportar_reporte_excel, name='reporte_excel'),
]