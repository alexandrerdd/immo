from django.db import models

# User Model
class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

# Gestion Model
class Gestion(models.Model):
    name = models.CharField(max_length=100)
    proprietor = models.CharField(max_length=100)
    proprietor_address = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name

# GestionUser Model
class GestionUser(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('assistant', 'Assistant'),
        ('viewer', 'Viewer'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'gestion')

    def __str__(self):
        return f"{self.user.username} - {self.gestion.name} ({self.role})"

# Bien Model
class Bien(models.Model):
    gestion = models.ForeignKey(Gestion, related_name="biens", on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    num_units = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.address

# Unit Model (Unite)
class Unit(models.Model):
    bien = models.ForeignKey(Bien, related_name="units", on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=50)
    #type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Unite {self.unit_number} - {self.bien.address}"

# Tenant Model
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=255, blank=True)
    rent_start_date = models.DateField()
    guarantee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_rent = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    contract = models.FileField(upload_to='contracts/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('current', 'Current'), ('old', 'Old')], default='current')

    def __str__(self):
        return self.name

# UnitTenant Model
class UnitTenant(models.Model):
    unit = models.ForeignKey(Unit, related_name="unit_tenants", on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, related_name="unit_tenants", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('current', 'Current'), ('old', 'Old')], default='current')

    def __str__(self):
        return f"{self.tenant.name} in {self.unit.unit_number} - {self.status}"

# Rent Payment Model
class RentPayment(models.Model):
    tenant = models.ForeignKey(Tenant, related_name="payments", on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, related_name="payments", on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant.name} for {self.unit.unit_number} on {self.date}"
    # python manage.py add_gestion_user 
    # python manage.py add_biens 
    # python manage.py add_units