from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from immo.models import Gestion, Bien, Unit, Tenant, RentPayment, UnitTenant, GestionUser, Group, GroupUser
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Gestion)
admin.site.register(Bien)
admin.site.register(Unit)
admin.site.register(Tenant)
admin.site.register(RentPayment)
admin.site.register(UnitTenant)
admin.site.register(GestionUser)
admin.site.register(Group)
admin.site.register(GroupUser)