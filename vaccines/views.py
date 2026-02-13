from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Vaccine
from .serializers import VaccineSerializer


class VaccineViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for vaccines.
    """

    queryset = Vaccine.objects.all().order_by("name")
    serializer_class = VaccineSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["manufacturer"]
    search_fields = ["name", "manufacturer"]
    ordering_fields = ["name", "created_at"]

