

# apps/orders/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateOrderSerializer, OrderSerializer
from .services import OrderService

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order = OrderService.create_order(
            user=request.user,
            validated_data=serializer.validated_data
        )
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders = OrderService.get_user_orders(request.user)
        return Response(OrderSerializer(orders, many=True).data)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_id):
        order = OrderService.get_order_by_id(request.user, order_id)
        if not order:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(OrderSerializer(order).data)