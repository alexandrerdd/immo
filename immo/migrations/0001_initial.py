# Generated by Django 4.2.23 on 2025-06-12 22:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('num_units', models.PositiveIntegerField(default=0)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('proprietor', models.CharField(max_length=100)),
                ('proprietor_address', models.TextField(blank=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True, unique=True)),
                ('phone', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
                ('Gestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='immo.gestion')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('status', models.CharField(choices=[('current', 'Current'), ('old', 'Old')], default='current', max_length=10)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_number', models.CharField(max_length=50)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='immo.bien')),
            ],
        ),
        migrations.CreateModel(
            name='UnitTenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent_start_date', models.DateField()),
                ('guarantee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('start_rent', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('current_rent', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('debt', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('contract', models.FileField(blank=True, null=True, upload_to='contracts/')),
                ('status', models.CharField(choices=[('current', 'Current'), ('old', 'Old')], default='current', max_length=10)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_tenants', to='immo.tenant')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_tenants', to='immo.unit')),
            ],
        ),
        migrations.CreateModel(
            name='RentPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
                ('UnitTenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rent_payments', to='immo.unittenant')),
            ],
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('manager', 'Manager'), ('assistant', 'Assistant'), ('viewer', 'Viewer')], max_length=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='immo.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'group')},
            },
        ),
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='custom_groups', through='immo.GroupUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GestionUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('manager', 'Manager'), ('assistant', 'Assistant'), ('viewer', 'Viewer')], max_length=10)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
                ('gestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='immo.gestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'gestion')},
            },
        ),
        migrations.AddField(
            model_name='gestion',
            name='users',
            field=models.ManyToManyField(related_name='gestions', through='immo.GestionUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bien',
            name='gestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biens', to='immo.gestion'),
        ),
    ]
