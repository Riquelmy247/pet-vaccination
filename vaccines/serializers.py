from rest_framework import serializers

from .models import Vaccine


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = [
            "id",
            "name",
            "manufacturer",
            "description",
            "periodicity_days",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

