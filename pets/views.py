from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Pet
from .permissions import IsPetOwner
from .serializers import PetSerializer


class PetViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for pets.
    Users can access only their own pets.
    """

    serializer_class = PetSerializer
    permission_classes = [IsPetOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["species", "breed"]
    search_fields = ["name", "breed"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        user = self.request.user
        return Pet.objects.filter(owner=user).order_by("name")

