# Contimapp/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o ambiente padrão de configurações do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Contimapp.settings')

app = Celery('Contimapp')

# Carrega configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre tarefas em todos os módulos de tarefas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
