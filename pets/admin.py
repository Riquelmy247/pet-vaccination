from django.contrib import admin

from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "species", "breed", "owner", "created_at")
    search_fields = ("name", "breed", "owner__full_name", "owner__email")
    list_filter = ("species",)

