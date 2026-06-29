from rest_framework import serializers
from products.models import Product
from recommendations.models import User, UserInteraction

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'description', 'image_url', 'created_at']
        

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']
    
    
# UserInteraction Serializer
class UserInteractionSerializer(serializers.ModelSerializer):
    # Show product and user details instead of just IDs
    product_details = ProductSerializer(source='product', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = UserInteraction
        fields = ['id', 'user', 'user_details', 'product', 'product_details', 
                  'interaction_type', 'rating', 'timestamp']


# Simplified interaction serializer for creating
class CreateUserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = ['user', 'product', 'interaction_type', 'rating']
        

class RecommendationResponseSerializer(serializers.Serializer):
    """Serializer for recommendation responses"""
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    score = serializers.FloatField()
    
    # Additional fields we'll add later
    category = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)