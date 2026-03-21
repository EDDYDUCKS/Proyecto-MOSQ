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
# 2. GENERADOR DE REPORTES EXCEL
# ==========================================

@api_view(['GET'])
@permission_classes([IsAdminUser]) # Candado: Solo los administradores pueden descargar esto
def exportar_reporte_excel(request):
    # 1. Creamos el archivo Excel en blanco
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte de Préstamos"

    # 2. Ponemos los encabezados exactos que pidió el Product Owner
    encabezados = [
        'Fecha de Entrega', 'Hora de Entrega', 'Fecha de Devolución', 'Hora de Devolución',
        'N° Carnet', 'Nombre del Estudiante', 'Carrera', 'Año', 
        'Descripción del Equipo', 'Cantidad', 'Entregado Por (Admin)', 'Recibido Por (Estudiante)'
    ]
    ws.append(encabezados)

    # 3. Traemos todos los préstamos de la base de datos
    prestamos = Prestamo.objects.all().select_related('estudiante', 'equipo', 'entregado_por')

    # 4. Llenamos las filas una por una
    for p in prestamos:
        # Formateamos las fechas y horas para que se vean bonitas
        fecha_p = p.fecha_prestamo.strftime('%Y-%m-%d') if p.fecha_prestamo else 'N/A'
        hora_p = p.fecha_prestamo.strftime('%H:%M:%S') if p.fecha_prestamo else 'N/A'
        fecha_d = p.fecha_devolucion.strftime('%Y-%m-%d') if p.fecha_devolucion else 'Pendiente'
        hora_d = p.fecha_devolucion.strftime('%H:%M:%S') if p.fecha_devolucion else 'Pendiente'
        
        # Sacamos el nombre del admin que entregó (si existe)
        entregado_por = p.entregado_por.username if p.entregado_por else 'N/A'

        # Armamos la fila
        fila = [
            fecha_p,
            hora_p,
            fecha_d,
            hora_d,
            p.estudiante.carnet or 'Sin registro',
            f"{p.estudiante.first_name} {p.estudiante.last_name}",
            p.estudiante.carrera or 'Sin registro',
            p.estudiante.ano_cursado or 'Sin registro',
            p.equipo.nombre,
            1, # La cantidad siempre es 1 por cada registro de préstamo
            entregado_por,
            p.estudiante.username
        ]
        ws.append(fila)

    # 5. Preparamos la respuesta para que el navegador descargue el archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Mensual_SGPED.xlsx"'
    
    # Guardamos y enviamos
    wb.save(response)
    return response