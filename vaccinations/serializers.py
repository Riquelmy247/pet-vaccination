from rest_framework import serializers

from pets.models import Pet
from vaccines.models import Vaccine

from .models import Vaccination


class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = [
            "id",
            "pet",
            "vaccine",
            "application_date",
            "next_due_date",
            "notes",
            "veterinarian_name",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_pet(self, value: Pet) -> Pet:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            if value.owner != request.user:
                raise serializers.ValidationError("You can only create vaccinations for your own pets.")
        return value

    def validate_vaccine(self, value: Vaccine) -> Vaccine:
        if not value:
            raise serializers.ValidationError("Vaccine is required.")
        return value

