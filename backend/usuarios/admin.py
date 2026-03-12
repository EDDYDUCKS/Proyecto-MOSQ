from django.contrib import admin
from .models import Estudiante, Equipo, Prestamo

# Le decimos al panel de admin que nos deje controlar estas tablas
admin.site.register(Estudiante)
admin.site.register(Equipo)
admin.site.register(Prestamo)