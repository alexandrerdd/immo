from django.contrib import admin
from immo.models import User, Gestion, Bien, Unit, Tenant, RentPayment, UnitTenant, GestionUser
admin.site.register(User)
admin.site.register(Gestion)
admin.site.register(Bien)
admin.site.register(Unit)
admin.site.register(Tenant)
admin.site.register(RentPayment)
admin.site.register(UnitTenant)
admin.site.register(GestionUser)