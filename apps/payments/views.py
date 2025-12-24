from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import CreatePaymentSerializer, PaymentSerializer
from .services import PaymentService

class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            payment = PaymentService.create_payment(
                user=request.user,
                validated_data=serializer.validated_data
            )
            
            # Simulate processing (in real app, this would be async)
            PaymentService.process_payment(payment.payment_id)
            
            return Response(
                PaymentSerializer(payment).data,
                status=status.HTTP_201_CREATED
            )
            
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class PaymentListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        payments = PaymentService.get_user_payments(request.user)
        return Response(PaymentSerializer(payments, many=True).data)

class PaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, payment_id):
        payment = PaymentService.get_payment_by_id(request.user, payment_id)
        if not payment:
            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(PaymentSerializer(payment).data)

# Webhook view for payment gateway callbacks
class PaymentWebhookView(APIView):
    """Receive payment status updates from payment gateway"""
    
    def post(self, request):
        # Verify webhook signature (implementation depends on payment gateway)
        # Update payment status based on webhook data
        
        return Response({"status": "received"}, status=status.HTTP_200_OK)