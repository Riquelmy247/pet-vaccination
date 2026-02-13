from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import VaccinationFilter
from .models import Vaccination
from .permissions import IsVaccinationPetOwner
from .serializers import VaccinationSerializer


class VaccinationViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for vaccinations.
    Users can access only vaccinations of their own pets.
    Supports filtering by pet, vaccine, and upcoming vaccinations.
    """

    serializer_class = VaccinationSerializer
    permission_classes = [IsVaccinationPetOwner]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = VaccinationFilter
    ordering_fields = ["application_date", "next_due_date", "created_at"]

    def get_queryset(self):
        user = self.request.user
        return (
            Vaccination.objects.select_related("pet", "vaccine")
            .filter(pet__owner=user)
            .order_by("-application_date")
        )

