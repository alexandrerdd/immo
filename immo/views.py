from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from immo.models import Gestion, Bien, Unit, Tenant, RentPayment, UnitTenant, GestionUser
from django import forms
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.db.models import Sum

class UserPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class GestionForm(forms.ModelForm):
    class Meta:
        model = Gestion
        fields = ['name', 'proprietor_address']

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        if password != password2:
            return HttpResponse("Passwords do not match.")
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered.")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect("login_view")
    
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        identifier = request.POST["identifier"]
        password = request.POST["password"]
        user = authenticate(request, username=identifier, password=password)
        if user is None:
            user = authenticate(request, email=identifier, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("welcome_view")
        else:
            return HttpResponse("Invalid credentials.")
    
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login_view")

def welcome_view(request):
    user = request.user
    gestion_users = GestionUser.objects.filter(user=user)
    gestions = [gu.gestion for gu in gestion_users]
    return render(request, "welcome/welcome.html", {"user": user, "gestions": gestions})

@login_required
def associer_user_gestion(request, gestion_id):
    gestion = Gestion.objects.get(id=gestion_id)
    users = User.objects.exclude(gestionuser__gestion=gestion)

    if request.method == 'POST':
        if 'user_id' in request.POST:
            user_id = request.POST['user_id']
            role = request.POST['role']
            user = User.objects.get(id=user_id)
            GestionUser.objects.create(user=user, gestion=gestion, role=role)
        elif 'new_username' in request.POST:
            username = request.POST['new_username']
            email = request.POST['new_email']
            password = request.POST['new_password']
            role = request.POST['new_role']
            user = User.objects.create_user(username=username, email=email, password=password)
            GestionUser.objects.create(user=user, gestion=gestion, role=role)
        return redirect('information_view', id=gestion_id)

    return render(request, 'templates_gestion_detail/informations/associer_user_gestion.html', {'gestion': gestion, 'users': users})

@login_required
def information_view(request, id):
    gestion = Gestion.objects.get(id=id)
    user = request.user
    is_manager = GestionUser.objects.filter(user=user, gestion=gestion, role='manager').exists()
    is_assistant = GestionUser.objects.filter(user=user, gestion=gestion, role='assistant').exists()

    if request.method == "POST":
        if 'add_user' in request.GET and is_manager:
            username = request.POST.get('username')
            role = request.POST.get('role')
            try:
                new_user = User.objects.get(username=username)
                GestionUser.objects.create(user=new_user, gestion=gestion, role=role)
            except User.DoesNotExist:
                return HttpResponse("User does not exist.")
        elif 'edit_user' in request.GET and is_manager:
            user_id = request.GET.get('edit_user')
            role = request.GET.get('role')
            try:
                gestion_user = GestionUser.objects.get(user_id=user_id, gestion=gestion)
                gestion_user.role = role
                gestion_user.save()
            except GestionUser.DoesNotExist:
                return HttpResponse("GestionUser does not exist.")
        elif 'delete_user' in request.GET and is_manager:
            user_id = request.GET.get('delete_user')
            try:
                gestion_user = GestionUser.objects.get(user_id=user_id, gestion=gestion)
                gestion_user.delete()
            except GestionUser.DoesNotExist:
                return HttpResponse("GestionUser does not exist.")
        elif 'update_role' in request.GET and is_manager:
            user_id = request.POST.get('user_id')
            role = request.POST.get('role')
            try:
                gestion_user = GestionUser.objects.get(user_id=user_id, gestion=gestion)
                gestion_user.role = role
                gestion_user.save()
            except GestionUser.DoesNotExist:
                return HttpResponse("GestionUser does not exist.")
        else:
            # Handle updates to proprietor, contact, and address fields
            field_name = request.POST.get('update_field')
            field_value = request.POST.get(field_name)
            if field_name in ['proprietor', 'contact', 'address']:
                setattr(gestion, field_name, field_value)
                gestion.save()

    password_form = UserPasswordForm(instance=user)
    gestion_form = GestionForm(instance=gestion)

    context = {
        "gestion": gestion,
        "user": user,
        "is_manager": is_manager,
        "is_assistant": is_assistant,
        "password_form": password_form,
        "gestion_form": gestion_form,
        "view_name": "information",
        "view_template": "templates_gestion_detail/informations/information.html",
    }

    return render(request, 'templates_gestion_detail/gestion_detail.html', context)

@login_required
def immeubles_view(request, id):
    gestion = Gestion.objects.get(id=id)
    biens = Bien.objects.filter(gestion=gestion)
    total_units = sum(bien.units.count() for bien in biens) or 0
    total_tenants = sum(unit.unit_tenants.filter(status='current').count() for bien in biens for unit in bien.units.all()) or 0
    total_rent = sum(payment.amount for bien in biens for unit in bien.units.all() for payment in unit.payments.filter(date__year=datetime.now().year)) or 0

    # Calculer la rentabilité de chaque bien
    for bien in biens:
        bien.total_rent = bien.units.aggregate(total_rent=Sum('payments__amount'))['total_rent'] or 0

    user = request.user
    context = {
        "gestion": gestion,
        "user": user,
        "biens": biens,
        "total_units": total_units,
        "total_tenants": total_tenants,
        "total_rent": total_rent,
        "view_name": "immeubles",
        "view_template": "templates_gestion_detail/immeubles/immeubles.html",
    }
    return render(request, 'templates_gestion_detail/gestion_detail.html', context)

@login_required
def locataires_view(request, id):
    gestion = Gestion.objects.get(id=id)
    user = request.user
    context = {
        "gestion": gestion,
        "user": user,
        "view_name": "locataires",
        "view_template": "templates_gestion_detail/locataires/locataires.html",
    }
    return render(request, 'templates_gestion_detail/gestion_detail.html', context)

@login_required
def paiement_du_loyer_view(request, id):
    bien_id = request.GET.get('bien')
    unit_id = request.GET.get('unit')
    tenant_id = request.GET.get('tenant')
    montant_min = request.GET.get('montant_min')
    montant_max = request.GET.get('montant_max')

    # Vérifiez si les paramètres sont valides et convertissez-les en entiers ou flottants
    try:
        bien_id = int(bien_id) if bien_id else None
        unit_id = int(unit_id) if unit_id else None
        tenant_id = int(tenant_id) if tenant_id else None
        montant_min = float(montant_min) if montant_min else None
        montant_max = float(montant_max) if montant_max else None
    except ValueError:
        return HttpResponse("Invalid parameters.")

    gestion = Gestion.objects.get(id=id)
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

    user = request.user
    context = {
        "gestion": gestion,
        "user": user,
        "payments": payments,
        "biens": biens,
        "tenants": tenants,
        "units": units,
        "view_name": "paiement_du_loyer",
        "view_template": "templates_gestion_detail/paiement_du_loyer/paiement_du_loyer.html",
    }
    return render(request, 'templates_gestion_detail/gestion_detail.html', context)

@login_required
def frais_view(request, id):
    gestion = Gestion.objects.get(id=id)
    user = request.user
    context = {
        "gestion": gestion,
        "user": user,
        "view_name": "frais",
        "view_template": "templates_gestion_detail/frais/frais.html",
    }
    return render(request, 'templates_gestion_detail/gestion_detail.html', context)

@login_required
def analyses_view(request, id):
    gestion = Gestion.objects.get(id=id)
    user = request.user
    context = {
        "gestion": gestion,
        "user": user,
        "view_name": "analyses",
        "view_template": "templates_gestion_detail/analyses/analyses.html",
    }
    return render(request, 'templates_gestion_detail/gestion_detail.html', context)

@login_required
def ia_local_view(request, id):
    gestion = Gestion.objects.get(id=id)
    user = request.user
    context = {
        "gestion": gestion,
        "user": user,
        "view_name": "ia_local",
        "view_template": "templates_gestion_detail/ia_local/ia_local.html",
    }
    return render(request, 'templates_gestion_detail/gestion_detail.html', context)

@login_required
def chat_gpt_view(request, id):
    gestion = Gestion.objects.get(id=id)
    user = request.user
    context = {
        "gestion": gestion,
        "user": user,
        "view_name": "chat_gpt",
        "view_template": "templates_gestion_detail/chat_gpt/chat_gpt.html",
    }
    return render(request, 'templates_gestion_detail/gestion_detail.html', context)

def get_units_by_bien(request):
    bien_id = request.GET.get('bien_id')
    if not bien_id:
        return JsonResponse({'error': 'Missing bien_id'}, status=400)
    try:
        units = Unit.objects.filter(bien_id=bien_id)
        units_data = [{'id': unit.id, 'unit_number': unit.unit_number} for unit in units]
        return JsonResponse({'units': units_data})
    except ValueError:
        return JsonResponse({'error': 'Invalid bien_id'}, status=400)

def get_tenants_by_bien(request):
    bien_id = request.GET.get('bien_id')
    if not bien_id:
        return JsonResponse({'error': 'Missing bien_id'}, status=400)
    try:
        tenants = Tenant.objects.filter(unit_tenants__unit__bien_id=bien_id).distinct()
        tenants_data = [{'id': tenant.id, 'name': tenant.name} for tenant in tenants]
        return JsonResponse({'tenants': tenants_data})
    except ValueError:
        return JsonResponse({'error': 'Invalid bien_id'}, status=400)

def get_bien_by_unit(request):
    unit_id = request.GET.get('unit_id')
    if not unit_id:
        return JsonResponse({'error': 'Missing unit_id'}, status=400)
    try:
        biens = Bien.objects.filter(units__id=unit_id).distinct()
        biens_data = [{'id': bien.id, 'address': bien.address} for bien in biens]
        return JsonResponse({'biens': biens_data})
    except ValueError:
        return JsonResponse({'error': 'Invalid unit_id'}, status=400)

def get_tenants_by_unit(request):
    unit_id = request.GET.get('unit_id')
    if not unit_id:
        return JsonResponse({'error': 'Missing unit_id'}, status=400)
    try:
        tenants = Tenant.objects.filter(unit_tenants__unit_id=unit_id).distinct()
        tenants_data = [{'id': tenant.id, 'name': tenant.name} for tenant in tenants]
        return JsonResponse({'tenants': tenants_data})
    except ValueError:
        return JsonResponse({'error': 'Invalid unit_id'}, status=400)

def get_biens_by_tenant(request):
    tenant_id = request.GET.get('tenant_id')
    if not tenant_id:
        return JsonResponse({'error': 'Missing tenant_id'}, status=400)
    try:
        biens = Bien.objects.filter(units__unit_tenants__tenant_id=tenant_id).distinct()
        biens_data = [{'id': bien.id, 'address': bien.address} for bien in biens]
        return JsonResponse({'biens': biens_data})
    except ValueError:
        return JsonResponse({'error': 'Invalid tenant_id'}, status=400)

def get_units_by_tenant(request):
    tenant_id = request.GET.get('tenant_id')
    if not tenant_id:
        return JsonResponse({'error': 'Missing tenant_id'}, status=400)
    try:
        units = Unit.objects.filter(unit_tenants__tenant_id=tenant_id).distinct()
        units_data = [{'id': unit.id, 'unit_number': unit.unit_number} for unit in units]
        return JsonResponse({'units': units_data})
    except ValueError:
        return JsonResponse({'error': 'Invalid tenant_id'}, status=400)