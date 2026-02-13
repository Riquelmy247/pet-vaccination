from django.contrib import admin

from .models import Vaccination


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pet",
        "vaccine",
        "application_date",
        "next_due_date",
        "veterinarian_name",
        "created_at",
    )
    search_fields = ("pet__name", "vaccine__name", "veterinarian_name")
    list_filter = ("vaccine", "application_date", "next_due_date")

