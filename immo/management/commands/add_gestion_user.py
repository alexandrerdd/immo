from django.core.management.base import BaseCommand
from immo.models import User, Gestion, GestionUser

class Command(BaseCommand):
    help = 'Add a gestion and an associated user with a role'

    def handle(self, *args, **kwargs):
        # Create the user
        user, created = User.objects.get_or_create(
            username='wanet',
            defaults={
                'email': 'josettewanet@gmail.com',
                'password': 'naevus769'  # Note: In a real application, make sure to hash the password
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {user.username} already exists'))

        # Create the gestion
        gestion, created = Gestion.objects.get_or_create(
            name='Wanet',
            proprietor=user,
            defaults={
                'proprietor_address': 'avenue isidore gerard 23'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created gestion {gestion.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Gestion {gestion.name} already exists'))

        # Assign role to the user in the gestion
        gestion_user, created = GestionUser.objects.get_or_create(
            user=user,
            gestion=gestion,
            defaults={
                'role': 'manager'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully assigned role to user {user.username} in gestion {gestion.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {user.username} already has a role in gestion {gestion.name}'))