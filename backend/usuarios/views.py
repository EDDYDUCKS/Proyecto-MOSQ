import openpyxl
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .models import Estudiante, Equipo, Prestamo
from .serializers import EstudianteSerializer, EquipoSerializer, PrestamoSerializer

# ==========================================
# 1. VISTAS AUTOMÁTICAS DE LA API (CRUD)
# ==========================================

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer


# ==========================================
# 2. GENERADOR DE REPORTES EXCEL (VERSIÓN CARRITO)
# ==========================================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def exportar_reporte_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte de Préstamos"

    encabezados = [
        'Fecha de Entrega', 'Hora de Entrega', 'Fecha de Devolución', 'Hora de Devolución',
        'N° Carnet', 'Nombre del Estudiante', 'Carrera', 'Año', 
        'Descripción del Equipo', 'Cantidad', 'Entregado Por (Admin)', 'Recibido Por (Estudiante)'
    ]
    ws.append(encabezados)

    # Traemos los tickets con todos sus detalles de un solo golpe para no saturar la base de datos
    prestamos = Prestamo.objects.all().select_related('estudiante', 'entregado_por').prefetch_related('detalles__equipo')

    for p in prestamos:
        fecha_p = p.fecha_prestamo.strftime('%Y-%m-%d') if p.fecha_prestamo else 'N/A'
        hora_p = p.fecha_prestamo.strftime('%H:%M:%S') if p.fecha_prestamo else 'N/A'
        fecha_d = p.fecha_devolucion.strftime('%Y-%m-%d') if p.fecha_devolucion else 'Pendiente'
        hora_d = p.fecha_devolucion.strftime('%H:%M:%S') if p.fecha_devolucion else 'Pendiente'
        entregado_por = p.entregado_por.username if p.entregado_por else 'N/A'

        # MAGIA: Recorremos cada línea del carrito para este ticket
        for detalle in p.detalles.all():
            fila = [
                fecha_p,
                hora_p,
                fecha_d,
                hora_d,
                p.estudiante.carnet or 'Sin registro',
                f"{p.estudiante.first_name} {p.estudiante.last_name}",
                p.estudiante.carrera or 'Sin registro',
                p.estudiante.ano_cursado or 'Sin registro',
                detalle.equipo.nombre, # El nombre de lo que prestó
                detalle.cantidad,      # <--- ¡LA CANTIDAD REAL!
                entregado_por,
                p.estudiante.username
            ]
            ws.append(fila)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Mensual_SGPED.xlsx"'
    
    wb.save(response)
    return response