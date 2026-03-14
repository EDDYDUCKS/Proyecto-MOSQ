from django.contrib import admin
from django.urls import path, include # <-- Ojo con agregar 'include' aquí

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conectamos las URLs de nuestra API para que entren por /api/
    path('api/', include('usuarios.urls')), 
]