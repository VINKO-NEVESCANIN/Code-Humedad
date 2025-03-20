from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

# Create your views here.
def upload_file(request):
  if request.method == "POST" and request.FILES.get("file"):
      upload_file = request.FILES["file"]
      fs = FileSystemStorage()
      fs.save(upload_file.name, upload_file)
      return HttpResponse("Archivo subido exitosamente")
  
  return render(request, "filtering/upload.html") # Renderizado de pagina HTML