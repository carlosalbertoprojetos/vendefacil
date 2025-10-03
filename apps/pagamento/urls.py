"""
URLs for pagamento app.
"""

from django.urls import path
from . import views

app_name = "pagamento"

urlpatterns = [
    path("", views.payment_home, name="home"),
    path("checkout/", views.checkout, name="checkout"),
    path("process/", views.process_payment, name="process"),
    path("success/", views.payment_success, name="success"),
    path("failure/", views.payment_failure, name="failure"),
]
