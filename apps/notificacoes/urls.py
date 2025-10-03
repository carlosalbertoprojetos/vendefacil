"""
URLs for notificacoes app.
"""

from django.urls import path
from . import views

app_name = 'notificacoes'

urlpatterns = [
    path('', views.notifications_home, name='home'),
    path('send/', views.send_notification, name='send'),
]
