from django.urls import path
from .views import CartView

urlpatterns = [
    
    path("create/", CartView.as_view(), name="cart"),
]

