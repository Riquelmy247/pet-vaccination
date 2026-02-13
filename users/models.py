from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom user manager that works with the existing `users` table.
    """

    def create_user(self, username: str, email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        username = username or email

        user = self.model(
            username=username,
            email=email,
            full_name=extra_fields.get("full_name", ""),
            phone_number=extra_fields.get("phone_number", ""),
            is_active=extra_fields.get("is_active", True),
            is_staff=extra_fields.get("is_staff", False),
            is_superuser=extra_fields.get("is_superuser", False),
            date_joined=extra_fields.get("date_joined", timezone.now()),
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing the pet owner (responsible person),
    mapped to the existing `users` table.
    """

    id = models.BigAutoField(primary_key=True)

    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = ["username"]

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.full_name or self.email

