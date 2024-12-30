from datetime import datetime
from immo.models import Gestion, Bien, Unit, RentPayment, Tenant, GestionUser
from django.db.models import Sum

def immeubles_view(gestion_id):
    gestion = Gestion.objects.get(id=gestion_id)
    biens = Bien.objects.filter(gestion=gestion)
    total_units = sum(bien.units.count() for bien in biens) or 0
    total_tenants = sum(unit.unit_tenants.filter(status='current').count() for bien in biens for unit in bien.units.all()) or 0
    total_rent = sum(payment.amount for bien in biens for unit in bien.units.all() for payment in unit.payments.filter(date__year=datetime.now().year)) or 0

    # Calculer la rentabilité de chaque bien
    for bien in biens:
        bien.total_rent = bien.units.aggregate(total_rent=Sum('payments__amount'))['total_rent'] or 0

    return gestion, biens, total_units, total_tenants, total_rent

def paiement_du_loyer_view(gestion_id, bien_id=None, unit_id=None, tenant_id=None, montant_min=None, montant_max=None):
    gestion = Gestion.objects.get(id=gestion_id)
    payments = RentPayment.objects.filter(unit__bien__gestion=gestion)

    # Appliquer les filtres un par un
    if bien_id:
        payments = payments.filter(unit__bien__id=bien_id)
    if unit_id:
        payments = payments.filter(unit__id=unit_id)
    if tenant_id:
        payments = payments.filter(tenant__id=tenant_id)
    if montant_min:
        payments = payments.filter(amount__gte=montant_min)
    if montant_max:
        payments = payments.filter(amount__lte=montant_max)

    # Récupérer les options pour les filtres (biens, locataires, etc.)
    biens = Bien.objects.filter(gestion=gestion)
    tenants = Tenant.objects.filter(status='current')
    units = Unit.objects.filter(bien__gestion=gestion)

    return gestion, payments, biens, tenants, units