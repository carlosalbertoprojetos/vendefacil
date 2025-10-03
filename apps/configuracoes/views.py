"""
Views for configuracoes app.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import role_required


@login_required
def settings_home(request):
    """Página inicial de configurações"""
    return render(request, 'configuracoes/home.html')


@role_required(['SUPERUSER'])
@login_required
def site_settings(request):
    """Configurações do site"""
    return render(request, 'configuracoes/site.html')


@role_required(['SUPERUSER', 'EMPRESA'])
@login_required
def empresa_settings(request):
    """Configurações da empresa"""
    return render(request, 'configuracoes/empresa.html')
