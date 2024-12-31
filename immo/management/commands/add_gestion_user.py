from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from immo.models import Gestion, GestionUser

class Command(BaseCommand):
    help = 'Add a gestion and an associated user with a role'

    def handle(self, *args, **kwargs):
        # Create the user
        user, created = User.objects.get_or_create(
            username='wanet',
            defaults={
                'email': 'josettewanet@gmail.com',
                'password': make_password('naevus769')  # Hash the password
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {user.username} already exists'))

        # Create the gestion
        gestion, created = Gestion.objects.get_or_create(
            name='Wanet',
            defaults={
                'proprietor': user.username,
                'proprietor_address': 'avenue isidore gerard 23',
                'email': user.email  # Add the email of the proprietor
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