from django.db import models
from products.models import Product


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    

class UserInteraction(models.Model):
    INTERACTION_CHOICES = [
        ('view', 'Viewed Product'),
        ('click', 'Clicked Product'),
        ('purchase', 'Purchased Product'),
        ('rating', 'Rated Product'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_CHOICES)
    rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        unique_together = ['user', 'product', 'timestamp']  # Prevents exact duplicates
    
    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.product.name}"