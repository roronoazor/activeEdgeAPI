import django_filters
from .models import *


class EmployeeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains")

    class Meta:
        model = Employee
        fields = {
            "first_name": ["icontains", "iexact"],
            "last_name": ["icontains", "iexact"],
            "join_date": ["exact", "gte", "lte"],

        }