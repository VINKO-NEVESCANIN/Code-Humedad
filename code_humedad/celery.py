from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps

# Configurar Django antes de cargar tareas
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'code_humedad.settings')

app = Celery('code_humedad')

# Cargar configuración desde Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodescubrimiento de tareas en todas las apps instaladas
app.autodiscover_tasks(lambda: [app_config.name for app_config in apps.get_app_configs()])

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
