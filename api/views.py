from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from products.models import Product
from recommendations.models import User, UserInteraction
from .serializers import (
    ProductSerializer,
    UserSerializer,
    UserInteractionSerializer,
    CreateUserInteractionSerializer
)

from rest_framework.exceptions import ValidationError
from recommendations.ml_service import RecommendationEngine



class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoints for products:
    - GET /api/products/          -> List all products
    - POST /api/products/         -> Create new product
    - GET /api/products/{id}/     -> Get single product
    - PUT /api/products/{id}/     -> Update product
    - DELETE /api/products/{id}/  -> Delete product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category', 'description']
    ordering_fields = ['price', 'created_at']


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoints for users:
    - GET /api/users/             -> List all users
    - POST /api/users/            -> Create new user
    - GET /api/users/{id}/        -> Get single user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        """
        Custom endpoint: GET /api/users/{id}/interactions/
        Returns all interactions for a specific user
        """
        user = self.get_object()
        interactions = user.interactions.all()
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)


class UserInteractionViewSet(viewsets.ModelViewSet):
    """
    API endpoints for user interactions:
    - GET /api/interactions/      -> List all interactions
    - POST /api/interactions/     -> Record new interaction
    - GET /api/interactions/{id}/ -> Get single interaction
    """
    queryset = UserInteraction.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']

    def get_serializer_class(self):
        """Use different serializer for creating vs reading"""
        if self.action == 'create':
            return CreateUserInteractionSerializer
        return UserInteractionSerializer

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """
        Filter interactions by user: GET /api/interactions/by_user/?user_id=1
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id parameter required'}, status=400)

        interactions = UserInteraction.objects.filter(user_id=user_id)
        serializer = UserInteractionSerializer(interactions, many=True)
        return Response(serializer.data)


class RecommendationViewSet(viewsets.ViewSet):
    """
    API endpoint for getting product recommendations.
    GET /api/recommendations/?user_id=1&count=10
    """
    
    def list(self, request):
        """
        Get recommendations for a user.
        
        Query Parameters:
        - user_id (required): The user to get recommendations for
        - count (optional): Number of recommendations (default: 10)
        - category (optional): Filter by product category
        - exclude_viewed (optional): Exclude products user already viewed (default: true)
        """
        
        # Get query parameters
        user_id = request.query_params.get('user_id')
        count = request.query_params.get('count', 10)
        category = request.query_params.get('category')
        exclude_viewed = request.query_params.get('exclude_viewed', 'true').lower() == 'true'
        
        # Validate user_id
        if not user_id:
            raise ValidationError({'error': 'user_id parameter is required'})
        
        try:
            user_id = int(user_id)
            count = int(count)
        except ValueError:
            raise ValidationError({'error': 'user_id and count must be integers'})
        
        # Check if user exists
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError({'error': f'User {user_id} does not exist'})
        
        try:
            # Load trained model
            engine = RecommendationEngine.load()
            
            # Get recommendations
            recommendations = engine.get_recommendations(
                user_id=user_id,
                num_recommendations=count,
                exclude_viewed=exclude_viewed
            )
            
            # Add product details (category, price)
            enriched_recommendations = []
            for rec in recommendations:
                try:
                    product = Product.objects.get(id=rec['product_id'])
                    enriched_rec = {
                        **rec,
                        'category': product.category,
                        'price': str(product.price)
                    }
                    enriched_recommendations.append(enriched_rec)
                except Product.DoesNotExist:
                    enriched_recommendations.append(rec)
            
            # Filter by category if provided
            if category:
                enriched_recommendations = [
                    rec for rec in enriched_recommendations 
                    if rec.get('category') == category
                ]
            
            # Serialize response
            response_data = {
                'user_id': user_id,
                'user_name': user.username,
                'count': len(enriched_recommendations),
                'recommendations': enriched_recommendations
            }
            
            return Response(response_data)
        
        except FileNotFoundError:
            return Response(
                {'error': 'Model not trained yet. Run: python manage.py train_recommendation_model'},
                status=400
            )
        except Exception as e:
            return Response(
                {'error': f'Error generating recommendations: {str(e)}'},
                status=500
            )