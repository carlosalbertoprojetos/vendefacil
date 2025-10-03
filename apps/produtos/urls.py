"""
URLs for produtos app.
"""

from django.urls import path
from . import views

app_name = "produtos"

urlpatterns = [
    path("", views.produto_list, name="list"),
    path("create/", views.produto_create, name="create"),
    path("<int:pk>/", views.produto_detail, name="detail"),
    path("<int:pk>/edit/", views.produto_edit, name="edit"),
    path("<int:pk>/delete/", views.produto_delete, name="delete"),
    path("categorias/", views.categoria_list, name="categoria_list"),
    path("ajax/get-subcategorias/", views.get_subcategorias, name="get_subcategorias"),
]
