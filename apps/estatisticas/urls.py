"""
URLs for estatisticas app.
"""

from django.urls import path
from . import views

app_name = 'estatisticas'

urlpatterns = [
    path('', views.stats_home, name='home'),
    path('produtos/', views.produto_stats, name='produtos'),
    path('pedidos/', views.pedido_stats, name='pedidos'),
]
