from django.core.management.base import BaseCommand
from recommendations.ml_service import RecommendationEngine


class Command(BaseCommand):
    help = 'Retrain recommendation model (useful for scheduled tasks)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force retrain even if model is recent',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔄 Retraining model...'))
        
        try:
            engine = RecommendationEngine()
            engine.prepare_data()
            engine.train()
            engine.save()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Model retrained successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )