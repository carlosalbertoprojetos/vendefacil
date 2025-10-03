"""
URLs for configuracoes app.
"""

from django.urls import path
from . import views

app_name = 'configuracoes'

urlpatterns = [
    path('', views.settings_home, name='home'),
    path('site/', views.site_settings, name='site'),
    path('empresa/', views.empresa_settings, name='empresa'),
]
