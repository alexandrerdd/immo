from django.core.management.base import BaseCommand
from immo.models import Bien, Gestion

class Command(BaseCommand):
    help = 'Add multiple biens to the database'

    def handle(self, *args, **kwargs):
        gestion = Gestion.objects.get(id=1)  # Assurez-vous que cette gestion existe

        biens_data = [
            {'address': 'Av Jean Volders 29', 'num_units': 6},
            {'address': 'Av Jean Volders 35', 'num_units': 6},
            {'address': 'Av des Gloires National 35 & 36', 'num_units': 2},
            {'address': 'Av Paul Segers 8', 'num_units': 4},
            {'address': 'Av Stiénon 34', 'num_units': 4},
            {'address': 'Av des Volontaires 154', 'num_units': 3},
            {'address': 'Rue de Tournai 2', 'num_units': 4},
            {'address': 'Bd Maurice Lemonnier 70', 'num_units': 1},
            {'address': 'Bd Maurice Lemonnier Coin 66', 'num_units': 6},
            {'address': 'Bd Maurice Lemonnier 66', 'num_units': 5},
            {'address': 'Bd Maurice Lemonnier 64', 'num_units': 11},
            {'address': 'Bd Maurice Lemonnier 60', 'num_units': 6},
            {'address': 'Bd Maurice Lemonnier 54', 'num_units': 10},
        ]

        for bien_data in biens_data:
            Bien.objects.create(gestion=gestion, **bien_data)

        self.stdout.write(self.style.SUCCESS('Successfully added biens'))

        # python manage.py add_gestion_user && python manage.py add_biens && python manage.py add_units && python manage.py add_tenants