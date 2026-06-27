from django.core.management.base import BaseCommand
from recommendations.ml_service import RecommendationEngine


class Command(BaseCommand):
    help = 'Train the recommendation model'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting model training...'))
        
        try:
            # Create engine
            engine = RecommendationEngine()
            
            # Prepare data
            engine.prepare_data()
            
            # Train
            engine.train()
            
            # Save
            engine.save()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Model training complete!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error training model: {str(e)}')
            )