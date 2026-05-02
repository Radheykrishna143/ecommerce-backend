from rest_framework.urls import path
from .views import (
    AddToCartView,
    CartView,
    UpdateCartItemView,
    PlaceOrderView,
    OrderHistoryView,
    OrderDetailView,
)

urlpatterns = [
    path("add/", AddToCartView.as_view()),
    path("", CartView.as_view()),
    path("update/<int:pk>/", UpdateCartItemView.as_view()),
    path("place-order/", PlaceOrderView.as_view()),
    path("orders/<int:pk>/", OrderDetailView.as_view()),
    path("orders/", OrderHistoryView.as_view()),
]
