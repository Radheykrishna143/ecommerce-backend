from rest_framework.urls import path
from .views import ProductDetailView, ProductListCreateView

urlpatterns = [
    path("", ProductListCreateView.as_view()),
    path("<int:pk>/", ProductDetailView.as_view()),
]
