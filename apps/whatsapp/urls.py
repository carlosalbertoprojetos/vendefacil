"""
URLs for whatsapp app.
"""

from django.urls import path
from . import views

app_name = 'whatsapp'

urlpatterns = [
    path('', views.whatsapp_home, name='home'),
    path('send/', views.send_message, name='send'),
    path('webhook/', views.webhook, name='webhook'),
]
