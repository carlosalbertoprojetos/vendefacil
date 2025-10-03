"""
URLs for pedidos app.
"""

from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    path("", views.pedido_list, name="list"),
    path("<int:pk>/", views.pedido_detail, name="detail"),
    path("<int:pk>/edit/", views.pedido_edit, name="edit"),
    path("<int:pk>/status/", views.pedido_status_update, name="status_update"),
    path("create/", views.pedido_create, name="create"),
]
