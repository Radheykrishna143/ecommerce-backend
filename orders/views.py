from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderItemSerializer, OrderSerializer
from products.models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404


# Create your views here.
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        product = Product.objects.get(id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": int(quantity)}
        )

        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()
        return Response(
            {
                "message": "Item added to cart",
                "product": product.name,
                "quantity": cart_item.quantity,
            }
        )


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()

        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)

        quantity = request.data.get("quantity")

        if quantity is None:
            return Response(
                {"error": "quantity is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        quantity = int(quantity)

        if quantity <= 0:
            cart_item.delete()
            return Response({"message": "Item removed from cart"})
        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Quantity updated"})


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        total_price = 0

        # calcualted
        for item in cart_items:
            total_price += item.product.price * item.quantity

        # create order
        order = Order.objects.create(user=request.user, total_price=total_price)

        # create order items
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {"error": f"Not enough stock for {item.product.name}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

            item.product.stock -= item.quantity
            item.product.save()

        # clear cart
        cart_items.delete()

        return Response(
            {
                "message": "Order placed successfully",
                "order_id": order.id,
                "total_price": order.total_price,
            }
        )


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
