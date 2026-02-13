from django.db import models


class Vaccine(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    periodicity_days = models.PositiveIntegerField(help_text="Recommended days between applications.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vaccines"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

