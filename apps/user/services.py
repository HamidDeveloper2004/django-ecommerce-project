from .models import User
from django.contrib.auth import authenticate
def register_user(validated_data):
    """
    Handles any additional business logic before or after user creation.
"""
from .models import User

def register_user(validated_data):
    user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password']
    )
    return user
def authenticate_user(email, password):
    
    user = authenticate(username=email, password=password)
    return user