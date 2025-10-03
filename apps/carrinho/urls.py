"""
URLs for carrinho app.
"""

from django.urls import path
from . import views

app_name = "carrinho"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("add/<int:produto_id>/", views.cart_add, name="add"),
    path("remove/<int:produto_id>/", views.cart_remove, name="remove"),
    path("update/<int:produto_id>/", views.cart_update, name="update"),
    path("clear/", views.cart_clear, name="clear"),
    # URLs AJAX
    path("remove-ajax/", views.cart_remove_ajax, name="remove_ajax"),
    path("update-ajax/", views.cart_update_ajax, name="update_ajax"),
]
