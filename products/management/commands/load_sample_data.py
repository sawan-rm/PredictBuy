from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from products.models import Product
from recommendations.models import User, UserInteraction


class Command(BaseCommand):
    help = 'Load sample data for development'

    def handle(self, *args, **options):
        fake = Faker()
        
        self.stdout.write(self.style.SUCCESS('Starting to load sample data...'))
        
        # Step 1: Create Products
        self.stdout.write('Creating products...')
        products = []
        categories = ['electronics', 'clothing', 'home', 'books', 'sports']
        
        for i in range(200):
            product = Product.objects.create(
                name=fake.word().capitalize() + ' ' + fake.word().capitalize(),
                category=random.choice(categories),
                price=round(random.uniform(10, 500), 2),
                description=fake.text(max_nb_chars=200),
                image_url=fake.image_url() if random.random() > 0.5 else None
            )
            products.append(product)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(products)} products'))
        
        # Step 2: Create Users
        self.stdout.write('Creating users...')
        users = []
        
        for i in range(100):
            user = User.objects.create(
                username=fake.user_name() + str(i),
                email=fake.email()
            )
            users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(users)} users'))
        
        # Step 3: Create User Interactions
        self.stdout.write('Creating user interactions...')
        interaction_types = ['view', 'click', 'purchase', 'rating']
        interaction_count = 0
        
        for user in users:
            # Each user interacts with 5-15 random products
            num_interactions = random.randint(5, 15)
            selected_products = random.sample(products, num_interactions)
            
            for product in selected_products:
                interaction_type = random.choice(interaction_types)
                rating = random.randint(1, 5) if interaction_type == 'rating' else None
                
                UserInteraction.objects.create(
                    user=user,
                    product=product,
                    interaction_type=interaction_type,
                    rating=rating,
                    timestamp=timezone.now() - timezone.timedelta(days=random.randint(0, 30))
                )
                interaction_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {interaction_count} interactions'))
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ Sample data loaded successfully!')
        )
        self.stdout.write(f'Products: {len(products)}')
        self.stdout.write(f'Users: {len(users)}')
        self.stdout.write(f'Interactions: {interaction_count}')