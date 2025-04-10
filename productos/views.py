
import pandas as pd
from django.shortcuts import render, redirect
from .models import Producto
from .forms import ExcelUploadForm, StockUploadForm, ReposicionUploadForm

def subir_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            df = pd.read_excel(archivo)

            for _, row in df.iterrows():
                cliente = str(row['cliente']).strip()
                codigo = str(row['codigo']).strip()
                descripcion = str(row['descripcion']).strip()
                cantidad = int(row['cantidad_por_caja'])

                Producto.objects.update_or_create(
                    cliente=cliente,
                    codigo=codigo,
                    defaults={
                        'descripcion': descripcion,
                        'cantidad_por_caja': cantidad
                    }
                )
            return redirect('subir_excel')
    else:
        form = ExcelUploadForm()
    return render(request, 'subir_excel.html', {'form': form})

def subir_stock(request):
    if request.method == 'POST':
        form = StockUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            cliente = form.cleaned_data['cliente']
            df = pd.read_excel(archivo)

            for _, row in df.iterrows():
                codigo = str(row['codigo']).strip()
                stock_total = int(row['stock_total'])
                stock_carrusel = int(row['stock_carrusel'])

                try:
                    producto = Producto.objects.get(cliente=cliente, codigo=codigo)
                    producto.stock_total = stock_total
                    producto.stock_carrusel = stock_carrusel
                    producto.save()
                except Producto.DoesNotExist:
                    pass
            return redirect('subir_stock')
    else:
        form = StockUploadForm()
    return render(request, 'subir_stock.html', {'form': form})

def subir_reposicion(request):
    if request.method == 'POST':
        form = ReposicionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            cliente = form.cleaned_data['cliente']
            df = pd.read_excel(archivo)

            for _, row in df.iterrows():
                codigo = str(row['codigo']).strip()
                promedio = int(row['promedio_venta'])
                tipo = str(row['tipo_ubicacion']).strip().lower()
                unidades_batea = int(row['unidades_por_batea'])

                stock_max = ((promedio + unidades_batea - 1) // unidades_batea) * unidades_batea

                try:
                    producto = Producto.objects.get(cliente=cliente, codigo=codigo)
                    producto.promedio_venta = promedio
                    producto.tipo_ubicacion = tipo
                    producto.unidades_por_batea = unidades_batea
                    producto.stock_max_carrusel = stock_max
                    producto.save()
                except Producto.DoesNotExist:
                    pass
            return redirect('subir_reposicion')
    else:
        form = ReposicionUploadForm()
    return render(request, 'subir_reposicion.html', {'form': form})
