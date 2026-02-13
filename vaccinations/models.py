from django.db import models

from pets.models import Pet
from vaccines.models import Vaccine


class Vaccination(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vaccinations")
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="vaccinations")
    application_date = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    veterinarian_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vaccinations"
        ordering = ["-application_date", "pet__name"]

    def __str__(self) -> str:
        return f"{self.pet} - {self.vaccine} on {self.application_date}"

