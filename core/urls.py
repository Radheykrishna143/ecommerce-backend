from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home(request):
    return Response(
        {"message": "Jai Shree RadheyKrishna", "user": request.user.username}
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    # user api
    path("api/users/", include("users.urls")),
    # jwt apis
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/", TokenRefreshView.as_view(), name="token_refresh"),
    # product apis
    path("api/products/", include("products.urls")),
    # cart api
    path("api/cart/", include("orders.urls")),
]
