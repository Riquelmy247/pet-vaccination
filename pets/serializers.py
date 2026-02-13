from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Pet

User = get_user_model()


class PetSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source="owner",
    )

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "species",
            "breed",
            "birth_date",
            "weight",
            "owner_id",
            "created_at",
        ]
        read_only_fields = ["id", "owner_id", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            raise serializers.ValidationError("Authenticated user is required to create a pet.")
        validated_data["owner"] = request.user
        return super().create(validated_data)

