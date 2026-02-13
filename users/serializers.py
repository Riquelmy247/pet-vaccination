from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone_number", "created_at"]
        read_only_fields = ["id", "created_at"]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone_number", "created_at"]
        read_only_fields = ["id", "email", "created_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone_number", "password", "password_confirm"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Password fields did not match."})
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm", None)
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            full_name=validated_data.get("full_name", ""),
            phone_number=validated_data.get("phone_number", ""),
        )
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        """
        After successful registration, return user data and JWT tokens.
        """
        data = UserSerializer(instance).data
        refresh = RefreshToken.for_user(instance)
        data["tokens"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return data

