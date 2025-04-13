
import pandas as pd
from django.shortcuts import render, redirect
from .models import Producto, UbicacionCarrusel
from .forms import ExcelUploadForm, ExcelUbicacionesForm
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import os
import shutil
from django.utils.timezone import now
from django.db.models import Count
from django.utils.safestring import mark_safe
from math import ceil
from openpyxl import Workbook
from collections import Counter

def subir_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            df = pd.read_excel(archivo)
            df.columns = df.columns.str.lower().str.strip()

            if 'cliente_codigo' not in df.columns:
                messages.error(request, "El archivo debe tener la columna 'cliente_codigo'.")
                return redirect('subir_excel')

            # Obtener todos los productos existentes
            existentes = set(Producto.objects.values_list('cliente_codigo', flat=True))

            nuevos = []
            actualizados = []

            for _, row in df.iterrows():
                cliente_codigo = str(row['cliente_codigo']).strip()

                datos = {}
                for columna in df.columns:
                    if columna != 'cliente_codigo' and not pd.isna(row[columna]):
                        datos[columna] = row[columna]

                if cliente_codigo in existentes:
                    Producto.objects.filter(cliente_codigo=cliente_codigo).update(**datos)
                    actualizados.append(cliente_codigo)
                else:
                    nuevos.append(Producto(cliente_codigo=cliente_codigo, **datos))

            if nuevos:
                Producto.objects.bulk_create(nuevos)

            mensaje = "✅ Archivo procesado con éxito. "
            if nuevos:
                mensaje += f"Se crearon {len(nuevos)} productos nuevos. "
            if actualizados:
                mensaje += f"Se actualizaron {len(actualizados)} productos existentes."

            messages.success(request, mensaje)
            return redirect('subir_excel')
    else:
        form = ExcelUploadForm()

    return render(request, 'subir_excel.html', {'form': form})


def descargar_plantilla(request):
    columnas = [
        'cliente_codigo', 'stock_total', 'stock_carrusel', 'cliente', 'codigo', 'descripcion', 
        'cantidad_por_caja', 'promedio_venta', 'promedio_sobredimensionado',
        'cantidad_op', 'tipo_ubicacion', 'unidades_por_batea', 'cantidad_bateas',
        'cantidad_max_bateas', 'stock_max_carrusel', 'psicofarmaco'
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

def editar_producto(request):
    producto = None
    valores = {}
    campos = [f.name for f in Producto._meta.fields if f.name != 'id']

    if request.method == 'POST':
        cliente_codigo = request.POST.get('cliente_codigo')
        if 'buscar' in request.POST:
            producto = Producto.objects.filter(cliente_codigo=cliente_codigo).first()
            if producto:
                valores = {campo: getattr(producto, campo) for campo in campos}
            else:
                messages.info(request, "🔍 No se encontró el producto. Podés cargarlo desde cero.")
                valores = {'cliente_codigo': cliente_codigo}
        elif 'guardar' in request.POST:
            datos = {campo: request.POST.get(campo) for campo in campos}
            producto, creado = Producto.objects.update_or_create(
                cliente_codigo=datos['cliente_codigo'],
                defaults=datos
            )
            mensaje = "✅ Producto actualizado correctamente." if not creado else "🆕 Producto creado exitosamente."
            messages.success(request, mensaje)
            return redirect('editar_producto')

    return render(request, 'editar_producto.html', {
        'campos': campos,
        'valores': valores
    })

def subir_ubicaciones(request):
    if request.method == 'POST':
        form = ExcelUbicacionesForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            df = pd.read_excel(archivo)
            df.columns = df.columns.str.strip().str.lower()

            # Reemplazo de NaN por valores seguros
            df = df.fillna({
                'stock': 0,
                'entrando': 0,
                'saliendo': 0,
                'denominación': '',
                'lote': '',
                'caducidad': '',
                'udc': '',
                'udsudc': 0,
                'última entrada': '',
                'anchura (mm)': 0,
                'profundidad (mm)': 0,
                'altura (mm)': 0,
                'zona': '',
                'equipo': '',
                'módulo': '',
                'nivel': '',
                'fondo': '',
                'artículo': '',
                'reservado art.': '',
                'reservado udc': '',
                'fija': '',
                'codbarras1': '',
                'udc reserva': '',
                'bloqueada': '',
                'impedir entrada': '',
                'impedir salida': '',
                'udp': '',
                'udsudp': 0,
                'tp. stock': '',
                'propietario': '',
            })

            registros = []
            for _, row in df.iterrows():
                registros.append(UbicacionCarrusel(
                    id_posicion=str(row.get('idposiciondetalle', '')).strip(),
                    ubicacion=str(row.get('ubicación', '')).strip(),
                    stock=int(row.get('stock', 0)),
                    entrando=int(row.get('entrando', 0)),
                    saliendo=int(row.get('saliendo', 0)),
                    denominacion=row.get('denominación', ''),
                    lote=row.get('lote', ''),
                    caducidad=row.get('caducidad', ''),
                    udc=row.get('udc', ''),
                    uds_udc=int(row.get('udsudc', 0)),
                    ultima_entrada=row.get('última entrada', ''),
                    anchura=float(row.get('anchura (mm)', 0)),
                    profundidad=float(row.get('profundidad (mm)', 0)),
                    altura=float(row.get('altura (mm)', 0)),
                    zona=row.get('zona', ''),
                    equipo=row.get('equipo', ''),
                    modulo=row.get('módulo', ''),
                    nivel=row.get('nivel', ''),
                    fondo=row.get('fondo', ''),
                    articulo=row.get('artículo', ''),
                    reservado_articulo=row.get('reservado art.', ''),
                    reservado_udc=row.get('reservado udc', ''),
                    fija=row.get('fija', ''),
                    cod_barras=row.get('codbarras1', ''),
                    udc_reserva=row.get('udc reserva', ''),
                    bloqueada=row.get('bloqueada', ''),
                    impedir_entrada=row.get('impedir entrada', ''),
                    impedir_salida=row.get('impedir salida', ''),
                    udp=row.get('udp', ''),
                    uds_udp=int(row.get('udsudp', 0)),
                    tipo_stock=row.get('tp. stock', ''),
                    propietario=row.get('propietario', ''),
                ))

            # Limpiamos la tabla antes de la carga
            UbicacionCarrusel.objects.all().delete()
            UbicacionCarrusel.objects.bulk_create(registros)

            messages.success(request, f"✅ {len(registros)} ubicaciones cargadas correctamente.")
            return redirect('subir_ubicaciones')
    else:
        form = ExcelUbicacionesForm()

    return render(request, 'subir_ubicaciones.html', {'form': form})

def analisis_ocupacion(request):
    datos = UbicacionCarrusel.objects.exclude(ubicacion__iendswith='i')

    # Clasificaciones en texto
    clasificaciones = {
        0: "Vacias",
        1: "Menor a 10%",
        2: "Entre 10% y 20%",
        3: "Entre 20% y 30%",
        4: "Entre 30% y 40%",
        5: "Entre 40% y 50%",
        6: "Entre 50% y 60%",
        7: "Entre 60% y 70%",
        8: "Entre 70% y 80%",
        9: "Entre 80% y 90%",
        10: "Entre 90% y 100%",
    }

    # Traducción de alturas
    altura_labels = {
        100: "SUELO",
        180: "UDC170",
        380: "UDC320"
    }

    # Inicializar conteo
    resultado = {altura: {clas: 0 for clas in clasificaciones.values()} for altura in altura_labels.values()}
    valores_grafico = {altura: [0] * len(clasificaciones) for altura in altura_labels.values()}

    for u in datos:
        try:
            porcentaje = ((u.stock or 0) / (u.uds_udc or 1)) * 100
        except ZeroDivisionError:
            porcentaje = 0

        if porcentaje > 100:
            messages.warning(request, f"⚠️ {u.ubicacion}: porcentaje mayor al 100% ({porcentaje:.2f}%)")
            continue

        if u.uds_udc == 0 or u.stock == 0:
            clase = 0
        else:
            clase = min(int(porcentaje // 10) + 1, 10)

        clas_texto = clasificaciones[clase]
        altura = altura_labels.get(int(u.altura), "Otra")

        resultado[altura][clas_texto] += 1
        valores_grafico[altura][clase] += 1

    etiquetas = list(clasificaciones.values())
    columnas = list(resultado.keys())

    # Preparar los datos para la tabla: [(etiqueta, [valores por columna])]
    filas = [(etiquetas[i], [valores_grafico[col][i] for col in columnas]) for i in range(len(etiquetas))]

    contexto = {
        'resultado': resultado,
        'columnas': columnas,
        'etiquetas': etiquetas,
        'datos_grafico': [[valores_grafico[col][i] for col in columnas] for i in range(len(etiquetas))],
        'filas': filas,
    }
    # Calcular promedios
    ocupaciones_general = []
    ocupaciones_altura = {
        "SUELO": [],
        "UDC170": [],
        "UDC320": [],
    }

    totales_por_altura = {
        "SUELO": 20,
        "UDC170": 336,
        "UDC320": 840,
    }

    for u in datos:
        if u.stock is not None and u.uds_udc:
            try:
                porcentaje = (u.stock / u.uds_udc) * 100
                if porcentaje <= 100:  # filtramos errores
                    ocupaciones_general.append(porcentaje)

                    altura = altura_labels.get(int(u.altura), None)
                    if altura in ocupaciones_altura:
                        ocupaciones_altura[altura].append(porcentaje)
            except ZeroDivisionError:
                continue

    # Ahora agregamos ceros donde faltan
    for altura in totales_por_altura:
        cantidad_actual = len(ocupaciones_altura[altura])
        faltantes = totales_por_altura[altura] - cantidad_actual
        if faltantes > 0:
            ocupaciones_altura[altura].extend([0] * faltantes)

    # Finalmente calculamos los promedios
    todas = ocupaciones_altura["SUELO"] + ocupaciones_altura["UDC170"] + ocupaciones_altura["UDC320"]

    promedios = {
        "General": round(sum(todas) / len(todas), 2),
        "SUELO": round(sum(ocupaciones_altura["SUELO"]) / len(ocupaciones_altura["SUELO"]), 2),
        "UDC170": round(sum(ocupaciones_altura["UDC170"]) / len(ocupaciones_altura["UDC170"]), 2),
        "UDC320": round(sum(ocupaciones_altura["UDC320"]) / len(ocupaciones_altura["UDC320"]), 2),
    }
    contexto['promedios'] = promedios
    return render(request, 'analisis_ocupacion.html', contexto)

def armar_reposicion(request):
    productos = Producto.objects.exclude(cliente__isnull=True).exclude(cliente="")

    # Variables de selección por defecto
    dias_opciones = [0, 1, 2, 3, 4, 5]
    alturas_opciones = ["SUELO", "UDC170", "UDC320"]
    clientes_opciones = sorted(productos.values_list('cliente', flat=True).distinct())

    dias_seleccionados = []
    alturas_seleccionadas = []
    clientes_seleccionados = []
    filtro_psico = 'TODOS'
    datos = []
    total_unidades = 0

    if request.method == 'POST':
        # Filtros
        filtro_psico = request.POST.get('psicofarmaco')
        if filtro_psico == 'SI':
            productos = productos.filter(psicofarmaco='SI')
        elif filtro_psico == 'NO':
            productos = productos.exclude(psicofarmaco='SI')

        dias_seleccionados = [int(d) for d in request.POST.getlist('dias')]
        alturas_seleccionadas = request.POST.getlist('alturas')
        clientes_seleccionados = request.POST.getlist('clientes')

        if alturas_seleccionadas:
            productos = productos.filter(tipo_ubicacion__in=alturas_seleccionadas)

        if clientes_seleccionados:
            productos = productos.filter(cliente__in=clientes_seleccionados)

        # Cálculo de reposición
        for p in productos:
            try:
                unidades_dia = p.promedio_sobredimensionado / 5 if p.promedio_sobredimensionado else 0
                dias_stock = round(p.stock_carrusel / unidades_dia) if unidades_dia else 0

                if dias_stock not in dias_seleccionados:
                    continue

                if p.stock_total < p.stock_max_carrusel - p.stock_carrusel:
                    cantidad = p.stock_total
                else:
                    faltante = p.stock_max_carrusel - p.stock_carrusel
                    cantidad = ((-(-faltante // p.cantidad_por_caja)) * p.cantidad_por_caja) if p.cantidad_por_caja else 0

                if cantidad > 0:
                    datos.append((p.cliente, p.codigo, cantidad))
            except:
                continue

        total_unidades = sum([fila[2] for fila in datos])

        if request.POST.get('accion') == 'descargar':
            wb = Workbook()
            ws = wb.active
            ws.append(['Cliente', 'Código', 'Cantidad a reponer'])
            for fila in datos:
                ws.append(fila)

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="reposicion_galys.xlsx"'
            wb.save(response)
            return response

    # Separar clientes en 2 columnas
    mitad = len(clientes_opciones) // 2
    clientes_col1 = clientes_opciones[:mitad]
    clientes_col2 = clientes_opciones[mitad:]

    return render(request, 'armar_reposicion.html', {
        'resultados': datos,
        'dias_opciones': dias_opciones,
        'alturas_opciones': alturas_opciones,
        'clientes_col1': clientes_col1,
        'clientes_col2': clientes_col2,
        'clientes_seleccionados': clientes_seleccionados,
        'dias_seleccionados': dias_seleccionados,
        'alturas_seleccionadas': alturas_seleccionadas,
        'psicofarmaco': filtro_psico,
        'cantidad_productos': len(datos),
        'cantidad_unidades': total_unidades
    })
