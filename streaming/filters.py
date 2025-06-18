import django_filters
from .models import *

import django_filters


from rest_framework import filters
from django.db.models import Q
from django.db import models


from rest_framework.filters import BaseFilterBackend 
from django.utils import timezone

from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime
import pytz
from django.utils.timezone import make_aware
from datetime import timezone
utc = timezone.utc
def parse_and_adjust_date(date_string, is_start_date=True):
    """
    Ajusta una fecha dada según sea la fecha inicial o final y la convierte a UTC usando Django.
    """
    date_format = "%Y-%m-%d"  # Formato de fecha esperado

    try:
        date_obj = datetime.strptime(date_string, date_format)
    except ValueError:
        raise ValueError(f"La fecha {date_string} no tiene el formato correcto {date_format}.")

    # Ajustar para la fecha inicial o final del día
    if is_start_date:
        date_obj = date_obj.replace(hour=0, minute=0, second=0)
    else:
        date_obj = date_obj.replace(hour=23, minute=59, second=59)

    # Asegurarnos de que la fecha sea timezone-aware
    return make_aware(date_obj, timezone.utc)

class DateTimeIntervalFilter(BaseFilterBackend):
    """
    Filtro personalizado para filtrar por intervalos de tiempo en campos DateTimeField.
    """
    def filter_queryset(self, request, queryset, view):
        # Obtener los parámetros de la URL
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        field_name = request.GET.get('field_name', 'fechacreacion')  # Campo predeterminado

        # Validar los parámetros necesarios
        if not hasattr(queryset.model, field_name):
            print(f"El campo {field_name} no existe en el modelo {queryset.model.__name__}.")
            return queryset

        # Ajustar las fechas si están disponibles
        start_date = parse_and_adjust_date(start_date, is_start_date=True) if start_date else None
        end_date = parse_and_adjust_date(end_date, is_start_date=False) if end_date else None

        print(f"Fechas ajustadas: start_date={start_date}, end_date={end_date}")

        # Verificar si el campo especificado es de tipo DateTimeField
        field = queryset.model._meta.get_field(field_name)
        if not isinstance(field, models.DateTimeField):
            print(f"El campo {field_name} no es un DateTimeField. Filtro no aplicado.")
            return queryset

        # Filtrar el queryset según las fechas
        if start_date and end_date:
            return queryset.filter(
                Q(**{f'{field_name}__gte': start_date}) & Q(**{f'{field_name}__lte': end_date})
            )
        elif start_date:
            return queryset.filter(Q(**{f'{field_name}__gte': start_date}))
        elif end_date:
            return queryset.filter(Q(**{f'{field_name}__lte': end_date}))

        print("No se aplicó ningún filtro porque no se especificaron fechas.")
        return queryset
    