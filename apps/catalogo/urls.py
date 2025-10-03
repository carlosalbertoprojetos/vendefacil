"""
URLs for catalogo app.
"""

from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.catalogo_list, name='list'),
    path('<int:vendedor_id>/', views.catalogo_vendedor, name='vendedor'),
    path('empresa/<int:empresa_id>/', views.catalogo_empresa, name='empresa'),
]
