import os
import pandas as pd
from .forms import UploadFileForm
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from urllib.parse import quote as urlquote
from urllib.parse import unquote


def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        # Leer el archivo con pandas (puedes usar csv, excel, etc.)
        df = pd.read_excel(file)  # o pd.read_csv(file) si es un CSV
        columns = df.columns.tolist()  # Obtenemos los nombres de las columnas

        # Generar el rango dinámicamente con el número de columnas
        column_range = range(1, len(columns) + 1)
        
        return render(request, "filtering/select_columns.html", {
            "column_range": column_range,
            "columns": columns,
            "file_path": file.name  # O puedes guardar el archivo de alguna manera para luego descargarlo
        })
    
    return render(request, "filtering/upload.html")
  
def highlight_temperatures(val, min_temp, max_temp):
    """Resalta valores fuera del rango aplicando estilos con Styler."""
    if isinstance(val, (int, float)):
        if val < min_temp:
            return 'background-color: yellow'  # Amarillo = Bajo el rango
        elif val > max_temp:
            return 'background-color: red'  # Rojo = Arriba del rango
    return ''

def process_file(request):
    if request.method == "POST":
        file_path = os.path.join(settings.MEDIA_ROOT, request.POST.get("file_path"))
        temp_columns = request.POST.getlist("temp_columns")  # Columnas seleccionadas
        min_temp = float(request.POST.get("min_temp"))
        max_temp = float(request.POST.get("max_temp"))

        df = pd.read_excel(file_path)

        # Aplicar estilos con Styler sin modificar los valores originales
        styled_df = df.style.applymap(lambda x: highlight_temperatures(x, min_temp, max_temp), subset=temp_columns)

        # Guardar el archivo con estilos en un Excel
        modified_file_path = os.path.join(settings.MEDIA_ROOT, "modified_" + os.path.basename(file_path))
        with pd.ExcelWriter(modified_file_path, engine='openpyxl') as writer:
            styled_df.to_excel(writer, index=False)
        
        return render(request, "filtering/download.html", {
            "modified_file": "modified_" + os.path.basename(file_path)
        })

    return HttpResponse("Método no permitido", status=405)
  
def download_file(request, filename):
    filename = unquote(filename)
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={urlquote(filename)}'
            return response
    else:
        return HttpResponse("El archivo no existe.", status=404)