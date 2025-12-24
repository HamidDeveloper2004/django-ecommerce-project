from apps.cart.models import Cart
from apps.products.models import Product

class CartService:
    @staticmethod
    def add_to_cart(user, product_id, quantity):
        # Fetch the product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValueError("Product does not exist")

        # Check if item already exists in cart
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            # If it exists, update the quantity
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item
    
    @staticmethod
    def get_cart_items(user):
        
        """Get all cart items for a user"""
        return Cart.objects.filter(user=user).select_related('product')
    
    @staticmethod  
    def remove_from_cart(user, product_id):
        """Remove item from cart"""
        try:
            product = Product.objects.get(id=product_id)
            cart_item = Cart.objects.get(user=user, product=product)
            cart_item.delete()
            return True
        except (Product.DoesNotExist, Cart.DoesNotExist):
            return False
    
    @staticmethod
    def update_cart_item(user, product_id, quantity):
        """Update cart item quantity"""
        try:
            product = Product.objects.get(id=product_id)
            cart_item = Cart.objects.get(user=user, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            return cart_item
        except (Product.DoesNotExist, Cart.DoesNotExist):
            return None