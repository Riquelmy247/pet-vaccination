from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserViewSet, RegisterView
from pets.views import PetViewSet
from vaccines.views import VaccineViewSet
from vaccinations.views import VaccinationViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"pets", PetViewSet, basename="pet")
router.register(r"vaccines", VaccineViewSet, basename="vaccine")
router.register(r"vaccinations", VaccinationViewSet, basename="vaccination")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/register/", RegisterView.as_view(), name="auth-register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="auth-login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
]

