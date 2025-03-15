from django.shortcuts import render
from .forms import UploadFileForm

# Create your views here.
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            # TODO: Procesar el archivo aqui
            return render(request, "upload.html", {"form": form, "success": True})
        else:
            form = UploadFileForm()
            
        return render(request, "upload.html", {'form': form})
    