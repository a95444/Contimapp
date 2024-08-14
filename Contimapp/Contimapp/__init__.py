# Contimapp/__init__.py

from __future__ import absolute_import, unicode_literals

# Certifique-se de que o aplicativo Celery é carregado quando o Django iniciar
from .celery import app as celery_app

__all__ = ('celery_app',)