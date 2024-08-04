from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, Discount, Product, Order, OrderItem
from .serializers import CategorySerializer, DiscountSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer

# Function-based detail view using APIView
class ProductDetailView(APIView):
    permission_classes = (IsAuthenticated,)  # Ensure the user is authenticated

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

# ModelViewSet for CRUD operations
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)  # Ensure the user is authenticated

class OrderDetailView(APIView):
    permission_classes = (IsAuthenticated,)  # Ensure the user is authenticated

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return Response(status=204)

# ModelViewSet for CRUD operations for Order
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)  # Ensure the user is authenticated

# ViewSet for CRUD operations for OrderItem
class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    permission_classes = (IsAuthenticated,)  # Ensure the user is authenticated

    def perform_create(self, serializer):
        # Custom logic before saving, if any
        serializer.save()  # This calls the save method of the serializer

    def perform_update(self, serializer):
        # Custom logic before updating, if any
        serializer.save()  # This calls the save method of the serializer

# ViewSet for CRUD operations for Discount
class DiscountViewSet(viewsets.ModelViewSet):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    permission_classes = (IsAuthenticated,)  # Ensure the user is authenticated

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)