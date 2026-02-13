from datetime import date

import django_filters

from .models import Vaccination


class VaccinationFilter(django_filters.FilterSet):
    pet = django_filters.NumberFilter(field_name="pet_id")
    vaccine = django_filters.NumberFilter(field_name="vaccine_id")
    upcoming = django_filters.BooleanFilter(method="filter_upcoming")

    class Meta:
        model = Vaccination
        fields = ["pet", "vaccine", "upcoming"]

    def filter_upcoming(self, queryset, name, value):
        if value:
            today = date.today()
            return queryset.filter(next_due_date__gte=today)
        return queryset

