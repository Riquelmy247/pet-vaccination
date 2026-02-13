from django.conf import settings
from django.db import models


class Pet(models.Model):
    SPECIES_CHOICES = [
        ("dog", "Dog"),
        ("cat", "Cat"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=255)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pets",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pets"
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.species})"

