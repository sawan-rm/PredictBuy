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
