# apps/orders/services.py
import uuid
from django.db import transaction
from .models import Order, OrderItem
from apps.cart.models import Cart
from apps.products.models import Product

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, validated_data):
        # Generate unique order number
        order_number = f"ORD-{uuid.uuid4().hex[:10].upper()}"
        
        # Calculate total from items
        items = validated_data['items']
        total_amount = 0
        
        # Create order
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            shipping_address=validated_data['shipping_address'],
            billing_address=validated_data['billing_address'],
            total_amount=0  # Will update after calculating
        )
        
        # Create order items and calculate total
        for item_data in items:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            
            total_amount += price * quantity
        
        # Update order total
        order.total_amount = total_amount
        order.save()
        
        # Clear user's cart after order
        Cart.objects.filter(user=user).delete()
        
        return order
    
    @staticmethod
    def get_user_orders(user):
        return Order.objects.filter(user=user).prefetch_related('items', 'items__product')
    
    @staticmethod
    def get_order_by_id(user, order_id):
        try:
            return Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return None
    
    @staticmethod
    def update_order_status(order_id, status):
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return order
        except Order.DoesNotExist:
            return None