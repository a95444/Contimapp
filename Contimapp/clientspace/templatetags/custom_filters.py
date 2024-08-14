from django import template
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import datetime

register = template.Library()

@register.filter
def format_datetime(value):
    local_dt = localtime(value)  # Ajusta para o fuso horário local
    return local_dt.strftime('%d/%m/%Y %H:%M')  # Formato dia/mês/ano horas:minutos