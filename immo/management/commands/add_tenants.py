from django.core.management.base import BaseCommand
from immo.models import Bien, Unit, Tenant, UnitTenant

class Command(BaseCommand):
    help = 'Add tenants to existing units in the database'

    def handle(self, *args, **kwargs):
        tenants_data = {
            'Av Jean Volders 29': [
                {'unit_number': 'Rez commercial', 'tenant_name': 'Tenant 1', 'status': 'current'},
                {'unit_number': 'étage 0,5', 'tenant_name': 'Tenant 2', 'status': 'current'},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 3', 'status': 'current'},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 4', 'status': 'current'},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 5', 'status': 'current'},
                {'unit_number': 'étage 4', 'tenant_name': 'Tenant 6', 'status': 'current'},
            ],
            'Av Jean Volders 35': [
                {'unit_number': 'Rez commercial', 'tenant_name': 'Tenant 7', 'status': 'current'},
                {'unit_number': 'étage 0,5', 'tenant_name': 'Tenant 8', 'status': 'current'},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 9', 'status': 'current'},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 10', 'status': 'current'},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 11', 'status': 'current'},
                {'unit_number': 'étage 4', 'tenant_name': 'Tenant 12', 'status': 'current'},
            ],
            'Av des Gloires National 35 & 36': [
                {'unit_number': 'Maison 35', 'tenant_name': 'Tenant 13', 'status': 'current'},
                {'unit_number': 'Maison 36', 'tenant_name': 'Tenant 14', 'status': 'current'},
            ],
            'Av Paul Segers 8': [
                {'unit_number': 'Rez de chaussée', 'tenant_name': 'Tenant 15', 'status': 'current'},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 16', 'status': 'current'},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 17', 'status': 'current'},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 18', 'status': 'current'},
            ],
            'Av Stiénon 34': [
                {'unit_number': 'Rez de chaussée', 'tenant_name': 'Tenant 19', 'status': 'current'},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 20', 'status': 'current'},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 21', 'status': 'current'},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 22', 'status': 'current'},
            ],
            'Av des Volontaires 154': [
                {'unit_number': 'Rez de chaussée', 'tenant_name': 'Tenant 23', 'status': 'current'},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 24', 'status': 'current'},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 25', 'status': 'current'},
            ],
            'Rue de Tournai 2': [
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 26', 'status': 'current'},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 27', 'status': 'current'},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 28', 'status': 'current'},
                {'unit_number': 'étage 4', 'tenant_name': 'Tenant 29', 'status': 'current'},
            ],
            'Bd Maurice Lemonnier 70': [
                {'unit_number': 'Rez commercial', 'tenant_name': 'Tenant 30', 'status': 'current'},
            ],
            'Bd Maurice Lemonnier Coin 66': [
                {'unit_number': 'Étage 1', 'tenant_name': 'Tenant 31', 'status': 'current'},
                {'unit_number': 'Étage 2', 'tenant_name': 'Tenant 32', 'status': 'current'},
                {'unit_number': 'Étage 3', 'tenant_name': 'Tenant 33', 'status': 'current'},
                {'unit_number': 'Étage 4, Chambre Sud', 'tenant_name': 'Tenant 34', 'status': 'current'},
                {'unit_number': 'étage 4, Chambre Nord', 'tenant_name': 'Tenant 35', 'status': 'current'},
            ],
            'Bd Maurice Lemonnier 66': [
                {'unit_number': 'bureau', 'tenant_name': 'Tenant 36', 'status': 'current'},
                {'unit_number': 'étage 2, chambre arrière', 'tenant_name': 'Tenant 37', 'status': 'current'},
                {'unit_number': 'étage 2, chambre avant', 'tenant_name': 'Tenant 38', 'status': 'current'},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 39', 'status': 'current'},
                {'unit_number': 'étage 4, chambre arrière', 'tenant_name': 'Tenant 40', 'status': 'current'},
                {'unit_number': 'étage 4, chambre avant', 'tenant_name': 'Tenant 41', 'status': 'current'},
            ],
            'Bd Maurice Lemonnier 64': [
                {'unit_number': 'Rez commercial', 'tenant_name': 'Tenant 42', 'status': 'current'},
                {'unit_number': 'étage 1, Chambre avant sud', 'tenant_name': 'Tenant 43', 'status': 'current'},
                {'unit_number': 'étage 1, Chambre avant nord', 'tenant_name': 'Tenant 44', 'status': 'current'},
                {'unit_number': 'étage 1, Chambre arrière', 'tenant_name': 'Tenant 45', 'status': 'current'},
                {'unit_number': 'étage 2, Chambre avant sud', 'tenant_name': 'Tenant 46', 'status': 'current'},
                {'unit_number': 'étage 2, Chambre avant nord', 'tenant_name': 'Tenant 47', 'status': 'current'},
                {'unit_number': 'étage 2, Chambre arrière', 'tenant_name': 'Tenant 48', 'status': 'current'},
                {'unit_number': 'étage 3, Chambre avant sud', 'tenant_name': 'Tenant 49', 'status': 'current'},
                {'unit_number': 'étage 3, Chambre avant nord', 'tenant_name': 'Tenant 50', 'status': 'current'},
                {'unit_number': 'étage 3, Chambre arrière', 'tenant_name': 'Tenant 51', 'status': 'current'},
            ],
            'Bd Maurice Lemonnier 60': [
                {'unit_number': 'rez commercial', 'tenant_name': 'Tenant 52', 'status': 'current'},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 53', 'status': 'current'},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 54', 'status': 'current'},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 55', 'status': 'current'},
                {'unit_number': 'étage 4, chambre avant', 'tenant_name': 'Tenant 56', 'status': 'current'},
                {'unit_number': 'étage 4, chambre arrière', 'tenant_name': 'Tenant 57', 'status': 'current'},
            ],
            'Bd Maurice Lemonnier 54': [
                {'unit_number': 'rez commercial', 'tenant_name': 'Tenant 58', 'status': 'current'},
                {'unit_number': 'étage 0,5', 'tenant_name': 'Tenant 59', 'status': 'current'},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 60', 'status': 'current'},
                {'unit_number': 'étage 1,5', 'tenant_name': 'Tenant 61', 'status': 'current'},
                {'unit_number': 'étage 2, chambre avant', 'tenant_name': 'Tenant 62', 'status': 'current'},
                {'unit_number': 'étage 2, chambre arrière', 'tenant_name': 'Tenant 63', 'status': 'current'},
                {'unit_number': 'étage 3, chambre avant', 'tenant_name': 'Tenant 64', 'status': 'current'},
                {'unit_number': 'étage 3, chambre arrière', 'tenant_name': 'Tenant 65', 'status': 'current'},
                {'unit_number': 'étage 4, chambre avant', 'tenant_name': 'Tenant 66', 'status': 'current'},
                {'unit_number': 'étage 4, chambre arrière', 'tenant_name': 'Tenant 67', 'status': 'current'},
            ],
        }

        for address, units in tenants_data.items():
            try:
                bien = Bien.objects.get(address=address)
                for unit_data in units:
                    unit = Unit.objects.get(bien=bien, unit_number=unit_data['unit_number'])
                    tenant, created = Tenant.objects.get_or_create(
                        name=unit_data['tenant_name'],
                        defaults={
                            'rent_start_date': '2024-01-01',
                            'current_rent': 100.00,
                            'debt': 0.00,
                            'guarantee': 200.00,
                            'contract': None,
                            'status': 'current'
                        }
                    )
                    UnitTenant.objects.create(unit=unit, tenant=tenant, status=unit_data['status'])
            except Bien.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Bien with address {address} does not exist'))
            except Unit.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Unit with unit number {unit_data["unit_number"]} in bien {address} does not exist'))

        self.stdout.write(self.style.SUCCESS('Successfully added tenants'))

from django.core.management.base import BaseCommand
from immo.models import Bien, Unit, Tenant, UnitTenant

class Command(BaseCommand):
    help = 'Add tenants to existing units in the database'

    def handle(self, *args, **kwargs):
        tenants_data = {
            'Av Jean Volders 29': [
                {'unit_number': 'Rez commercial', 'tenant_name': 'Tenant 1', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 0,5', 'tenant_name': 'Tenant 2', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 3', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 4', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 5', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 4', 'tenant_name': 'Tenant 6', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Av Jean Volders 35': [
                {'unit_number': 'Rez commercial', 'tenant_name': 'Tenant 7', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 0,5', 'tenant_name': 'Tenant 8', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 9', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 10', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 11', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 4', 'tenant_name': 'Tenant 12', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Av des Gloires National 35 & 36': [
                {'unit_number': 'Maison 35', 'tenant_name': 'Tenant 13', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'Maison 36', 'tenant_name': 'Tenant 14', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Av Paul Segers 8': [
                {'unit_number': 'Rez de chaussée', 'tenant_name': 'Tenant 15', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 16', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 17', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 18', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Av Stiénon 34': [
                {'unit_number': 'Rez de chaussée', 'tenant_name': 'Tenant 19', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 20', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 21', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 22', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Av des Volontaires 154': [
                {'unit_number': 'Rez de chaussée', 'tenant_name': 'Tenant 23', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 24', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 25', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Rue de Tournai 2': [
                {'unit_number': 'étage 1', 'tenant_name': 'Tenant 26', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2', 'tenant_name': 'Tenant 27', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 28', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 4', 'tenant_name': 'Tenant 29', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Bd Maurice Lemonnier 70': [
                {'unit_number': 'Rez commercial', 'tenant_name': 'Tenant 30', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Bd Maurice Lemonnier Coin 66': [
                {'unit_number': 'Étage 1', 'tenant_name': 'Tenant 31', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'Étage 2', 'tenant_name': 'Tenant 32', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'Étage 3', 'tenant_name': 'Tenant 33', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'Étage 4, Chambre Sud', 'tenant_name': 'Tenant 34', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 4, Chambre Nord', 'tenant_name': 'Tenant 35', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Bd Maurice Lemonnier 66': [
                {'unit_number': 'bureau', 'tenant_name': 'Tenant 36', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2, chambre arrière', 'tenant_name': 'Tenant 37', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2, chambre avant', 'tenant_name': 'Tenant 38', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 3', 'tenant_name': 'Tenant 39', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 4, chambre arrière', 'tenant_name': 'Tenant 40', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 4, chambre avant', 'tenant_name': 'Tenant 41', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
            ],
            'Bd Maurice Lemonnier 64': [
                {'unit_number': 'Rez commercial', 'tenant_name': 'Tenant 42', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 1, Chambre avant sud', 'tenant_name': 'Tenant 43', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 1, Chambre avant nord', 'tenant_name': 'Tenant 44', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 1, Chambre arrière', 'tenant_name': 'Tenant 45', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2, Chambre avant sud', 'tenant_name': 'Tenant 46', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2, Chambre avant nord', 'tenant_name': 'Tenant 47', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 2, Chambre arrière', 'tenant_name': 'Tenant 48', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 3, Chambre avant sud', 'tenant_name': 'Tenant 49', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 3, Chambre avant nord', 'tenant_name': 'Tenant 50', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
                {'unit_number': 'étage 3, Chambre arrière', 'tenant_name': 'Tenant 51', 'status': 'current', 'rent_start_date': '2024-01-01', 'guarantee': 200.00, 'start_rent': 100.00, 'current_rent': 100.00, 'debt': 0.00},
