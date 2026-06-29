import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from datetime import datetime

from products.models import Product
from recommendations.models import User, UserInteraction


class RecommendationEngine:
    """
    Collaborative filtering recommendation system.
    Learns from user interactions and recommends products.
    """

    def __init__(self):
        self.user_product_matrix = None
        self.user_similarity_matrix = None
        self.users_list = None
        self.products_list = None
        self.interaction_weights = {
            'view': 1,
            'click': 1,
            'purchase': 3,
            'rating': 2
        }

    def prepare_data(self):
        """
        Fetch interactions from database and create user-product matrix.
        """
        print("📊 Preparing data...")

        # Get all users and products
        self.users_list = list(User.objects.all().order_by('id'))
        self.products_list = list(Product.objects.all().order_by('id'))

        print(
            f"   Found {len(self.users_list)} users and {len(self.products_list)} products")

        # Create user-product matrix
        # These lists will later help us find the correct row and column in the matrix.
        user_ids = [u.id for u in self.users_list]
        product_ids = [p.id for p in self.products_list]

        # user_index = {
        #     user_id: idx
        #     for idx, user_id in enumerate(user_ids)
        # }
        # product_index = {
        #     product_id: idx
        #     for idx, product_id in enumerate(product_ids)
        # }
        
        # Initialize matrix with zeros
        # 1. Use np.array() to convert existing Python data (like a list) into a NumPy array for math.
        # 2. Use np.zeros() to create a blank, empty placeholder array of a specific shape to fill later.
        matrix = np.zeros((len(self.users_list), len(self.products_list)))

        # Fetch all interactions
        interactions = UserInteraction.objects.all()

        # Fill matrix with weighted interaction values
        for interaction in interactions:
            user_idx = user_ids.index(interaction.user_id)
            product_idx = product_ids.index(interaction.product_id)
            # user_idx = user_index[interaction.user_id]
            # product_idx = product_index[interaction.product_id]
            weight = self.interaction_weights.get(
                interaction.interaction_type, 1)
            matrix[user_idx, product_idx] += weight

        self.user_product_matrix = matrix
        print(
            f"   Created matrix: {matrix.shape[0]} users × {matrix.shape[1]} products")
        return self

    def train(self):
        """
        Calculate similarity between users using cosine similarity.
        """
        print("🧠 Training model...")

        if self.user_product_matrix is None:
            raise ValueError("Call prepare_data() first!")

        # Calculate cosine similarity between users
        # This shows how similar each user is to every other user
        
        # Cosine similarity measures how much two vectors point in the same direction.
        # If they point in exactly the same direction → similarity = 1
        # If they are unrelated → similarity ≈ 0
        # If they point in opposite directions → similarity = -1
        # In recommendation systems, similarities are usually between 0 and 1 because interaction values are non-negative.
        self.user_similarity_matrix = cosine_similarity(
            self.user_product_matrix)

        print(f"   Model trained!")
        print(
            f"   Similarity matrix shape: {self.user_similarity_matrix.shape}")
        return self

    def get_recommendations(self, user_id, num_recommendations=10, exclude_viewed=True):
        """
        Get product recommendations for a specific user.

        Args:
            user_id: ID of the user to recommend for
            num_recommendations: How many products to recommend
            exclude_viewed: Whether to exclude products user already viewed

        Returns:
            List of (product_id, recommendation_score) tuples
        """
        # Find user index
        user_ids = [u.id for u in self.users_list]
        
        
        if self.user_similarity_matrix is None:
                raise ValueError(
                "Model not trained. Call prepare_data() and train() first."
            )
        if self.user_product_matrix is None:
            raise ValueError(
                "User-product matrix not available."
            )


        try:
            user_idx = user_ids.index(user_id)
        except ValueError:
            raise ValueError(f"User {user_id} not found")

        # Get similarity scores with other users
        user_similarities = self.user_similarity_matrix[user_idx]

        # Get products user has already interacted with
        user_obj = User.objects.get(id=user_id)
        viewed_product_ids = set(
            user_obj.interactions.values_list('product_id', flat=True)
        )

        # Calculate recommendation scores
        recommendation_scores = np.zeros(len(self.products_list))

        total_similarity = 0
        for other_user_idx, similarity in enumerate(user_similarities):
            if similarity <= 0 or other_user_idx == user_idx:
                continue

            # Get products that similar user liked
            other_user_products = self.user_product_matrix[other_user_idx]

            # Add weighted scores
            recommendation_scores += similarity * other_user_products
            total_similarity += similarity
            
        if total_similarity > 0:
            recommendation_scores /= total_similarity
            
            
        # Exclude already viewed products if requested
        if exclude_viewed:
            product_ids = [p.id for p in self.products_list]
            for product_id in viewed_product_ids:
                if product_id in product_ids:
                    product_idx = product_ids.index(product_id)
                    recommendation_scores[product_idx] = -1

        # Get top N recommendations
        top_indices = np.argsort(recommendation_scores)[
            ::-1][:num_recommendations]

        recommendations = []
        for idx in top_indices:
            score = recommendation_scores[idx]
            if score > 0:
                product = self.products_list[idx]
                recommendations.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'score': float(score)
                })

        return recommendations

    def save(self, filepath='ml_models/recommendation_model.pkl'):
        """
        Save trained model to disk.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        model_data = {
            'user_product_matrix': self.user_product_matrix,
            'user_similarity_matrix': self.user_similarity_matrix,
            'users_list': self.users_list,
            'products_list': self.products_list,
            'interaction_weights': self.interaction_weights,
            'trained_at': datetime.now().isoformat()
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"✅ Model saved to {filepath}")

    @staticmethod
    def load(filepath='ml_models/recommendation_model.pkl'):
        """
        Load trained model from disk.
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        engine = RecommendationEngine()
        
        engine.user_product_matrix = model_data['user_product_matrix']
        engine.user_similarity_matrix = model_data['user_similarity_matrix']
        engine.users_list = model_data['users_list']
        engine.products_list = model_data['products_list']
        engine.interaction_weights = model_data['interaction_weights']

        print(f"✅ Model loaded from {filepath}")
        return engine
