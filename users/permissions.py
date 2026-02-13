from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import View

User = get_user_model()


class IsSelfOrAdmin(BasePermission):
    """
    Allows access only to the requested user object itself or admins.
    List endpoint is restricted to staff users.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in SAFE_METHODS and getattr(view, "action", None) == "list":
            return bool(request.user and request.user.is_staff)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        if not isinstance(obj, User):
            return False
        if request.user.is_staff:
            return True
        return obj == request.user

