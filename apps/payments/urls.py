from django.urls import path
from .views import PaymentCreateView, PaymentListView, PaymentDetailView, PaymentWebhookView

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('create/', PaymentCreateView.as_view(), name='payment-create'),
    path('<str:payment_id>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('webhook/', PaymentWebhookView.as_view(), name='payment-webhook'),
]