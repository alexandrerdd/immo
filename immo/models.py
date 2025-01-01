from django.db import models
from django.contrib.auth.models import User

# GroupUser Model (intermédiaire)
class GroupUser(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('assistant', 'Assistant'),
        ('viewer', 'Viewer'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'group')
    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.role})"

#group model
class Group(models.Model):
    name = models.CharField(max_length=100)
    Gestion = models.ForeignKey('Gestion', on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True, default=None)
    users = models.ManyToManyField(User, through=GroupUser, related_name="custom_groups", blank=True)
    
    def __str__(self):
        return self.name
    
# Gestion Model
class Gestion(models.Model):
    name = models.CharField(max_length=100)
    proprietor = models.CharField(max_length=100)
    proprietor_address = models.TextField(blank=True)
    email = models.EmailField(unique=True, blank=True, null=True, default=None)
    phone = models.CharField(max_length=20, blank=True, null=True, default=None)
    comment = models.TextField(blank=True, null=True, default=None)
    users = models.ManyToManyField(User, through='GestionUser', related_name='gestions')

    def __str__(self):
        return self.name

# GestionUser Model (intermédiaire)
class GestionUser(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('assistant', 'Assistant'),
        ('viewer', 'Viewer'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    comment = models.TextField(blank=True, null=True, default=None)

    class Meta:
        unique_together = ('user', 'gestion')

    def __str__(self):
        return f"{self.user.username} - {self.gestion.name} ({self.role})"

# Bien Model
class Bien(models.Model):
    gestion = models.ForeignKey(Gestion, related_name="biens", on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    num_units = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True, null=True, default=None)
    def __str__(self):
        return self.address

# Unit Model (Unite)
class Unit(models.Model):
    bien = models.ForeignKey(Bien, related_name="units", on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=50)
    type = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return f"Unite {self.unit_number} - {self.bien.address}"

# Tenant Model
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)
    status = models.CharField(max_length=10, choices=[('current', 'Current'), ('old', 'Old')], default='current')
    comment = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return self.name

# UnitTenant Model
class UnitTenant(models.Model):
    unit = models.ForeignKey(Unit, related_name="unit_tenants", on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, related_name="unit_tenants", on_delete=models.CASCADE)
    rent_start_date = models.DateField()
    guarantee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_rent = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    current_rent = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    contract = models.FileField(upload_to='contracts/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('current', 'Current'), ('old', 'Old')], default='current')
    comment = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.tenant.name} in {self.unit.unit_number} - {self.status}"

# Rent Payment Model
class RentPayment(models.Model):
    UnitTenant = models.ForeignKey(UnitTenant, related_name="rent_payments", on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    comment = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant.name} for {self.unit.unit_number} on {self.date}"