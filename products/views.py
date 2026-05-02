from .serializers import ProductSerializer
from rest_framework import generics
from .models import Product
from .permissions import isAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [isAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["price"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [isAdminOrReadOnly]
