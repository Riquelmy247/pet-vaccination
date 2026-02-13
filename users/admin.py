from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "phone_number", "is_staff", "created_at")
    search_fields = ("full_name", "email", "phone_number")
    list_filter = ("is_staff", "is_superuser", "is_active")

