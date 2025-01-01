from django.core.management.base import BaseCommand
from immo.models import Bien, Unit

class Command(BaseCommand):
    help = 'Add units to existing biens in the database'

    def handle(self, *args, **kwargs):
        units_data = {
            'Av Jean Volders 29': ['Rez commercial', 'étage 0,5', 'étage 1', 'étage 2', 'étage 3', 'étage 4'],
            'Av Jean Volders 35': ['Rez commercial', 'étage 0,5', 'étage 1', 'étage 2', 'étage 3', 'étage 4'],
            'Av des Gloires National 35 & 36': ['Maison 35', 'Maison 36'],
            'Av Paul Segers 8': ['Rez de chaussée', 'étage 1', 'étage 2', 'étage 3'],
            'Av Stiénon 34': ['Rez de chaussée', 'étage 1', 'étage 2', 'étage 3'],
            'Av des Volontaires 154': ['Rez de chaussée', 'étage 1', 'étage 2'],
            'Rue de Tournai 2': ['étage 1', 'étage 2', 'étage 3', 'étage 4'],
            'Bd Maurice Lemonnier 70': ['Rez commercial'],
            'Bd Maurice Lemonnier Coin 66': ['Étage 1', 'Étage 2', 'Étage 3', 'Étage 4, Chambre Sud', 'étage 4, Chambre Nord'],
            'Bd Maurice Lemonnier 66': ['bureau', 'étage 2, chambre arrière', 'étage 2, chambre avant', 'étage 3', 'étage 4, chambre arrière', 'étage 4, chambre avant'],
            'Bd Maurice Lemonnier 64': ['Rez commercial', 'étage 1, Chambre avant sud', 'étage 1, Chambre avant nord', 'étage 1, Chambre arrière', 'étage 2, Chambre avant sud', 'étage 2, Chambre avant nord', 'étage 2, Chambre arrière', 'étage 3, Chambre avant sud', 'étage 3, Chambre avant nord', 'étage 3, Chambre arrière', 'étage 4, Chambre avant sud', 'étage 4, Chambre avant nord', 'étage 4, Chambre arrière', 'étage 5, Chambre sud', 'étage 5, Chambre nord'],
            'Bd Maurice Lemonnier 60': ['rez commercial', 'étage 1', 'étage 2', 'étage 3', 'étage 4, chambre avant', 'étage 4, chambre arrière'],
            'Bd Maurice Lemonnier 54': ['rez commercial', 'étage 0,5', 'étage 1', 'étage 1,5', 'étage 2, chambre avant', 'étage 2, chambre arrière', 'étage 3, chambre avant', 'étage 3, chambre arrière', 'étage 4, chambre avant', 'étage 4, chambre arrière', 'étage 4,5 chambre avant', 'étage 4,5 chambre arrière'],
        }

        for address, units in units_data.items():
            try:
                bien = Bien.objects.get(address=address)
                for unit_name in units:
                    Unit.objects.create(bien=bien, unit_number=unit_name)
            except Bien.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Bien with address {address} does not exist'))

        self.stdout.write(self.style.SUCCESS('Successfully added units'))