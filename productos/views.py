
import pandas as pd
from django.shortcuts import render, redirect
from .models import Producto
from .forms import ExcelUploadForm
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import os
import shutil
from django.utils.timezone import now

def subir_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            df = pd.read_excel(archivo)
            df.columns = df.columns.str.lower().str.strip()

            if 'cliente_codigo' not in df.columns:
                return HttpResponse("El archivo debe tener la columna 'cliente_codigo'", status=400)

            for _, row in df.iterrows():
                cliente_codigo = str(row['cliente_codigo']).strip()

                producto, creado = Producto.objects.update_or_create(
                    cliente_codigo=cliente_codigo,
                    defaults={}
                )

                for columna in df.columns:
                    if columna != 'cliente_codigo' and not pd.isna(row[columna]):
                        setattr(producto, columna, row[columna])

                producto.save()

            return redirect('subir_excel')
    else:
        form = ExcelUploadForm()
    return render(request, 'subir_excel.html', {'form': form})

def descargar_plantilla(request):
    columnas = [
        'cliente_codigo', 'stock_total', 'stock_carrusel', 'cliente', 'codigo', 'descripcion', 
        'cantidad_por_caja', 'promedio_venta', 'promedio_sobredimensionado',
        'cantidad_op', 'tipo_ubicacion', 'unidades_por_batea', 'cantidad_bateas',
        'cantidad_max_bateas',  'psicofarmaco'
    ]
    df = pd.DataFrame(columns=columnas)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=plantilla_RepoGalys.xlsx'
    return response

def inicio(request):
    return render(request, 'inicio.html')

def crear_backup(request):
    # Calcular la raíz del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    origen = os.path.join(base_dir, 'db.sqlite3')
    print("🎯 Ejecutando función crear_backup")
    # Si la carpeta backups está en la raíz del proyecto, esta línea es correcta:
    backup_dir = os.path.join(base_dir, 'backups')
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = now().strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(backup_dir, f"backup_{timestamp}.sqlite3")

    shutil.copy(origen, destino)
    messages.success(request, f"Copia de seguridad creada: backup_{timestamp}.sqlite3")
    return HttpResponseRedirect('/')