from django.db import models

# Create your models here.

class ArchivoExcel(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='excel_files/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class RegistroTemperatura(models.Model):
    archivo = models.ForeignKey(ArchivoExcel, on_delete=models.CASCADE, related_name='registros')
    fecha_medicion = models.DateTimeField()
    temperatura = models.FloatField()
    sensor_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fecha_medicion} - {self.temperatura}°C"
