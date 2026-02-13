from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View

from .models import Vaccination


class IsVaccinationPetOwner(BasePermission):
    """
    Allows access only to vaccinations of pets owned by the authenticated user.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: View, obj: Vaccination) -> bool:
        return obj.pet.owner == request.user

