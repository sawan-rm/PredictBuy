from django.test import TestCase
from rest_framework.test import APIClient
from products.models import Product
from recommendations.models import User, UserInteraction


class RecommendationAPITestCase(TestCase):
    
    def setUp(self):
        """Create test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create(username='testuser', email='test@example.com')
        
        # Create test products
        self.product1 = Product.objects.create(
            name='Product 1',
            category='electronics',
            price=100.00,
            description='Test product 1'
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            category='clothing',
            price=50.00,
            description='Test product 2'
        )
        
        # Create user interaction
        UserInteraction.objects.create(
            user=self.user,
            product=self.product1,
            interaction_type='view'
        )
    
    def test_product_list(self):
        """Test getting list of products"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
    
    def test_create_product(self):
        """Test creating a product"""
        data = {
            'name': 'New Product',
            'category': 'electronics',
            'price': 299.99,
            'description': 'A new test product'
        }
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_user_creation(self):
        """Test creating a user"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com'
        }
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_record_interaction(self):
        """Test recording user interaction"""
        data = {
            'user': self.user.id,
            'product': self.product1.id,
            'interaction_type': 'purchase'
        }
        response = self.client.post('/api/interactions/', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_user_interactions_endpoint(self):
        """Test getting user's interactions"""
        response = self.client.get(f'/api/users/{self.user.id}/interactions/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)
    
    def test_recommendations_missing_user_id(self):
        """Test recommendations without user_id"""
        response = self.client.get('/api/recommendations/')
        self.assertEqual(response.status_code, 400)
    
    def test_recommendations_invalid_user(self):
        """Test recommendations for non-existent user"""
        response = self.client.get('/api/recommendations/?user_id=9999')
        self.assertEqual(response.status_code, 400)