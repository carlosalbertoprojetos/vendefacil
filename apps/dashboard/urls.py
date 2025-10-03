"""
URLs for dashboard app.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('empresa/', views.empresa_dashboard, name='empresa'),
    path('vendedor/', views.vendedor_dashboard, name='vendedor'),
    path('admin/', views.admin_dashboard, name='admin'),
]
