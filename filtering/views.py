import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        upload_file = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(upload_file.name, upload_file)
        file_path = fs.path(filename)

        # Leer el archivo con pandas
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            return HttpResponse(f"Error al leer el archivo: {str(e)}")

        # Extraer nombres de columnas
        columnas = df.columns.tolist()

        return render(request, "filtering/select_columns.html", {
            "file_path": filename,
            "columnas": columnas
        })

    return render(request, "filtering/upload.html")

def highlight_temperatures(val, min_temp, max_temp):
    """Resalta valores fuera del rango."""
    if isinstance(val, (int, float)):
        if val < min_temp:
            return 'background-color: yellow'  # Amarillo = Bajo el rango
        elif val > max_temp:
            return 'background-color: red'  # Rojo = Arriba del rango
    return ''

def process_file(request):
    if request.method == "POST":
        file_path = os.path.join(settings.MEDIA_ROOT, request.POST.get("file_path"))
        temp_columns = request.POST.getlist("temp_columns")  # Ahora obtenemos varias columnas
        min_temp = float(request.POST.get("min_temp"))
        max_temp = float(request.POST.get("max_temp"))

        df = pd.read_excel(file_path)

        # Aplicamos el resaltado en cada columna seleccionada
        for col in temp_columns:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: highlight_temperatures(x, min_temp, max_temp))

        # Guardamos el archivo modificado
        modified_file_path = os.path.join(settings.MEDIA_ROOT, "modified_" + os.path.basename(file_path))
        df.to_excel(modified_file_path, index=False)

        return render(request, "filtering/download.html", {
            "modified_file": "modified_" + os.path.basename(file_path)
        })

    return HttpResponse("Método no permitido", status=405)