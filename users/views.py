from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsSelfOrAdmin
from .serializers import RegisterSerializer, UserDetailSerializer, UserSerializer

User = get_user_model()


class RegisterView(APIView):
    """
    Public endpoint to register a new user (pet owner).
    """

    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.to_representation(user)
        return Response(data, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Read-only viewset for users.
    - List: restricted to staff users.
    - Retrieve: user can view only their own details (or any user if staff).
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrAdmin]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return super().get_serializer_class()

