from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from immo.models import User, Gestion, Bien, Unit, Tenant, RentPayment, UnitTenant, GestionUser
from django import forms
from immo.fct_gest import immeubles_view, paiement_du_loyer_view
from django.http import JsonResponse, HttpResponse
import json

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
        
        user = User.objects.create(username=username, email=email, password=password)
        return redirect("login_view")
    
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        identifier = request.POST["identifier"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=identifier, password=password)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=identifier, password=password)
            except User.DoesNotExist:
                return HttpResponse("Invalid credentials.")
        
        request.session['user_id'] = user.id
        return redirect("welcome_view")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login_view")

def welcome_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect("login_view")
    user = User.objects.get(id=user_id)
    gestion_users = GestionUser.objects.filter(user=user)
    gestions = [gu.gestion for gu in gestion_users]
    return render(request, "welcome/welcome.html", {"user": user, "gestions": gestions})

def associer_user_gestion(request, gestion_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login_view')

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
            user = User.objects.create(username=username, email=email, password=password)
            user.save()
            GestionUser.objects.create(user=user, gestion=gestion, role=role)
        return redirect('gestion_detail', id=gestion_id)

    return render(request, 'templates_gestion_detail/informations/associer_user_gestion.html', {'gestion': gestion, 'users': users})

def gestion_detail(request, id):
    gestion = Gestion.objects.get(id=id)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect("login_view")
    user = User.objects.get(id=user_id)
    is_manager = GestionUser.objects.filter(user=user, gestion=gestion, role='manager').exists()
    is_assistant = GestionUser.objects.filter(user=user, gestion=gestion, role='assistant').exists()
    view_name = request.GET.get('view', 'information')

    # Mapping view names to template paths
    view_templates = {
        'information': 'templates_gestion_detail/informations/information.html',
        'immeubles': 'templates_gestion_detail/immeubles/immeubles.html',
        'locataires': 'templates_gestion_detail/locataires/locataires.html',
        'paiement_du_loyer': 'templates_gestion_detail/paiement_du_loyer/paiement_du_loyer.html',
        'frais': 'templates_gestion_detail/frais/frais.html',
        'analyses': 'templates_gestion_detail/analyses/analyses.html',
        'ia_local': 'templates_gestion_detail/ia_local/ia_local.html',
        'chat_gpt': 'templates_gestion_detail/chat_gpt/chat_gpt.html',
    }
    view_template = view_templates.get(view_name, 'templates_gestion_detail/informations/information.html')

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
        elif 'update_bien' in request.GET and is_manager:
            try:
                data = json.loads(request.body)
                bien_id = data.get('bien_id')
                address = data.get('address')
                bien = Bien.objects.get(id=bien_id, gestion=gestion)
                bien.address = address
                bien.save()
                return JsonResponse({'success': True})
            except Bien.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Bien does not exist'})
        elif 'delete_bien' in request.GET and is_manager:
            try:
                data = json.loads(request.body)
                bien_id = data.get('bien_id')
                bien = Bien.objects.get(id=bien_id, gestion=gestion)
                bien.delete()
                return JsonResponse({'success': True})
            except Bien.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Bien does not exist'})
        else:
            # Handle updates to proprietor, contact, and address fields
            field_name = request.POST.get('update_field')
            field_value = request.POST.get(field_name)
            if field_name in ['proprietor', 'contact', 'address']:
                setattr(gestion, field_name, field_value)
                gestion.save()

    # Appel de la fonction immeubles_view
    if view_name == 'paiement_du_loyer':
        bien_id = request.GET.get('bien')
        unit_id = request.GET.get('unit')
        tenant_id = request.GET.get('tenant')
        montant_min = request.GET.get('montant_min')
        montant_max = request.GET.get('montant_max')
        gestion, payments, biens, tenants, units = paiement_du_loyer_view(id, bien_id, unit_id, tenant_id, montant_min, montant_max)
    else:
        gestion, biens, total_units, total_tenants, total_rent = immeubles_view(id)

    password_form = UserPasswordForm(instance=user)
    gestion_form = GestionForm(instance=gestion)

    context = {
        "gestion": gestion,
        "user": user,
        "is_manager": is_manager,
        "is_assistant": is_assistant,
        "view_name": view_name,
        "view_template": view_template,
        "password_form": password_form,
        "gestion_form": gestion_form,
    }

    if view_name == 'paiement_du_loyer':
        context.update({
            "payments": payments,
            "biens": biens,
            "tenants": tenants,
            "units": units,
        })
    else:
        context.update({
            "biens": biens,
            "total_units": total_units,
            "total_tenants": total_tenants,
            "total_rent": total_rent,
        })

    return render(request, "templates_gestion_detail/gestion_detail.html", context)

def get_units_by_bien(request):
    bien_id = request.GET.get('bien_id')
    units = Unit.objects.filter(bien_id=bien_id)
    units_data = [{'id': unit.id, 'unit_number': unit.unit_number} for unit in units]
    return JsonResponse({'units': units_data})

def get_tenants_by_bien(request):
    bien_id = request.GET.get('bien_id')
    tenants = Tenant.objects.filter(unit_tenants__unit__bien_id=bien_id).distinct()
    tenants_data = [{'id': tenant.id, 'name': tenant.name} for tenant in tenants]
    return JsonResponse({'tenants': tenants_data})

def get_units_and_tenants_by_unit(request):
    unit_id = request.GET.get('unit_id')
    units = Unit.objects.filter(id=unit_id)
    units_data = [{'id': unit.id, 'unit_number': unit.unit_number} for unit in units]
    tenants = Tenant.objects.filter(unit_tenants__unit_id=unit_id).distinct()
    tenants_data = [{'id': tenant.id, 'name': tenant.name} for tenant in tenants]
    return JsonResponse({'units': units_data, 'tenants': tenants_data})

def get_biens_and_tenants_by_tenant(request):
    tenant_id = request.GET.get('tenant_id')
    units = Unit.objects.filter(unit_tenants__tenant_id=tenant_id).distinct()
    units_data = [{'id': unit.id, 'unit_number': unit.unit_number} for unit in units]
    biens = Bien.objects.filter(units__unit_tenants__tenant_id=tenant_id).distinct()
    biens_data = [{'id': bien.id, 'address': bien.address} for bien in biens]
    return JsonResponse({'units': units_data, 'biens': biens_data})