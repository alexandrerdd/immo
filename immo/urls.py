"""
URL configuration for immo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from immo.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name="register_view"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('welcome/', welcome_view, name="welcome_view"),
    path('gestion/<int:id>/information/', information_view, name="information_view"),
    path('gestion/<int:id>/immeubles/', immeubles_view, name="immeubles_view"),
    path('gestion/<int:id>/locataires/', locataires_view, name="locataires_view"),
    path('gestion/<int:id>/paiement_du_loyer/', paiement_du_loyer_view, name="paiement_du_loyer_view"),
    path('gestion/<int:id>/frais/', frais_view, name="frais_view"),
    path('gestion/<int:id>/analyses/', analyses_view, name="analyses_view"),
    path('gestion/<int:id>/ia_local/', ia_local_view, name="ia_local_view"),
    path('gestion/<int:id>/chat_gpt/', chat_gpt_view, name="chat_gpt_view"),
    path('associer_user_gestion/<int:gestion_id>/', associer_user_gestion, name='associer_user_gestion'),
    path('paiements/', paiement_du_loyer_view, name='paiement_du_loyer'),
    path('get_units_by_bien/', get_units_by_bien, name='get_units_by_bien'),
    path('get_tenants_by_bien/', get_tenants_by_bien, name='get_tenants_by_bien'),
    path('get_bien_by_unit/', get_bien_by_unit, name='get_bien_by_unit'),
    path('get_tenants_by_unit/', get_tenants_by_unit, name='get_tenants_by_unit'),
    path('get_biens_by_tenant/', get_biens_by_tenant, name='get_biens_by_tenant'),
    path('get_units_by_tenant/', get_units_by_tenant, name='get_units_by_tenant'),
]
    
