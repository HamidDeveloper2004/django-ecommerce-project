from .models import Product

class ProductService:

    @staticmethod
    def create_product(validated_data):
        return Product.objects.create(**validated_data)

    @staticmethod
    def list_products():
        return Product.objects.filter(is_active=True).order_by('-created_at')
