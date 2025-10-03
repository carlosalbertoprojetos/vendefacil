"""
Views for estatisticas app.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def stats_home(request):
    """Página inicial de estatísticas"""
    return render(request, 'estatisticas/home.html')


@login_required
def produto_stats(request):
    """Estatísticas de produtos"""
    return render(request, 'estatisticas/produtos.html')


@login_required
def pedido_stats(request):
    """Estatísticas de pedidos"""
    return render(request, 'estatisticas/pedidos.html')
