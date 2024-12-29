from datetime import datetime
from immo.models import Gestion, Bien, Unit, RentPayment, UnitTenant, GestionUser
from django.db.models import Sum

def immeubles_view(gestion_id):
    gestion = Gestion.objects.get(id=gestion_id)
    print(gestion)
    biens = Bien.objects.filter(gestion=gestion)
    total_units = sum(bien.units.count() for bien in biens) or 0
    total_tenants = sum(unit.unit_tenants.filter(status='current').count() for bien in biens for unit in bien.units.all()) or 0
    total_rent = sum(payment.amount for bien in biens for unit in bien.units.all() for payment in unit.payments.filter(date__year=datetime.now().year)) or 0

    # Calculer la rentabilité de chaque bien
    for bien in biens:
        bien.total_rent = bien.units.aggregate(total_rent=Sum('payments__amount'))['total_rent'] or 0

    return gestion, biens, total_units, total_tenants, total_rent