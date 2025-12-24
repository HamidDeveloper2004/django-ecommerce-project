# apps/payments/services.py
import uuid
from django.db import transaction
from .models import Payment
from apps.orders.models import Order

class PaymentService:
    @staticmethod
    @transaction.atomic
    def create_payment(user, validated_data):
        order_id = validated_data['order_id']
        payment_method = validated_data['payment_method']
        
        # Get the order
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            raise ValueError("Order not found or doesn't belong to user")
        
        # Check if payment already exists
        if hasattr(order, 'payment'):
            raise ValueError("Payment already exists for this order")
        
        # Use order amount or provided amount
        amount = validated_data.get('amount', order.total_amount)
        
        # Create payment
        payment = Payment.objects.create(
            order=order,
            user=user,
            amount=amount,
            payment_method=payment_method,
            currency='USD'  # Could be dynamic
        )
        
        # Here you would integrate with payment gateway (Stripe, PayPal, etc.)
        # For now, we'll simulate payment processing
        
        return payment
    
    @staticmethod
    def process_payment(payment_id):
        """Simulate payment processing"""
        try:
            payment = Payment.objects.get(payment_id=payment_id)
            
            # Simulate payment processing logic
            # In real implementation, this would call payment gateway API
            
            if payment.status == 'pending':
                # Simulate successful payment 90% of the time
                import random
                if random.random() < 0.9:  # 90% success rate
                    payment.status = 'completed'
                    payment.transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
                else:
                    payment.status = 'failed'
                
                payment.save()
                return payment
            
            return payment
            
        except Payment.DoesNotExist:
            raise ValueError("Payment not found")
    
    @staticmethod
    def get_user_payments(user):
        return Payment.objects.filter(user=user).select_related('order')
    
    @staticmethod
    def get_payment_by_id(user, payment_id):
        try:
            return Payment.objects.get(payment_id=payment_id, user=user)
        except Payment.DoesNotExist:
            return None