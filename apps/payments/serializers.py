# apps/payments/serializers.py
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    order_total = serializers.DecimalField(source='order.total_amount', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'payment_id', 'order', 'order_number', 'order_total',
            'amount', 'currency', 'payment_method', 'status',
            'transaction_id', 'payment_date', 'completed_at'
        ]
        read_only_fields = ['payment_id', 'status', 'transaction_id', 'payment_date', 'completed_at']

class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHOD_CHOICES)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    
    def validate(self, data):
        # Add custom validation if needed
        return data

class PaymentWebhookSerializer(serializers.Serializer):
    """For payment gateway webhooks"""
    payment_id = serializers.CharField()
    status = serializers.CharField()
    transaction_id = serializers.CharField(required=False)
    metadata = serializers.JSONField(required=False)