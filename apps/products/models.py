from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    active = models.BooleanField(default=True)  # Fixed: removed 'if' and '='
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.name  # Fixed: return self.name not set1.name