from datetime import datetime

from rest_framework import filters
from rest_framework.compat import coreapi, coreschema


class CardFilterBackend(filters.BaseFilterBackend):

    def get_schema_fields(self, view):
        '''Настривает отображение GET параметров'''
        return [
            coreapi.Field(
                name='from_datetime',
                location='query',
                required=False,
                schema=coreschema.String(description='2018-01-31-18-01')
            ),
            coreapi.Field(
                name='to_datetime',
                location='query',
                required=False,
                schema=coreschema.String(description='2018-01-31-20-01')
            ),
            coreapi.Field(
                name='interval',
                location='query',
                required=False,
                schema=coreschema.String(
                    description='1, 12 или 24 (одно значение)'
                )
            )]

    def filter_queryset(self, request, queryset, view):
        '''Фильтр для работы с GET параметрами в запросе'''
        datetime_format = '%Y-%m-%d-%H-%M'
        from_datetime = request.query_params.get('from_datetime')
        to_datetime = request.query_params.get('to_datetime')
        interval = request.query_params.get('interval')
        if (from_datetime and to_datetime) is not None:
            queryset = queryset.filter(
                date__range=(
                    datetime.strptime(from_datetime, datetime_format),
                    datetime.strptime(to_datetime, datetime_format)
                )
            )
        elif from_datetime is not None:
            queryset = queryset.filter(
                date__gte=datetime.strptime(from_datetime, datetime_format)
            )
        if interval is not None:
            queryset = queryset[::int(interval)]
        return queryset
