"""
URL configuration for VendaSimples project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API
    path("api/v1/", include("apps.api.v1.urls")),
    # Authentication
    path("auth/", include("apps.authentication.urls")),
    path(
        "accounts/", include("apps.authentication.accounts_urls")
    ),  # Alias para compatibilidade
    # Dashboard
    path("dashboard/", include("apps.dashboard.urls")),
    # Products
    path("produtos/", include("apps.produtos.urls")),
    # Orders
    path("pedidos/", include("apps.pedidos.urls")),
    # Cart
    path("carrinho/", include("apps.carrinho.urls")),
    # Payment
    path("pagamento/", include("apps.pagamento.urls")),
    # Catalog
    path("catalogo/", include("apps.catalogo.urls")),
    # Settings
    path("configuracoes/", include("apps.configuracoes.urls")),
    # WhatsApp
    path("whatsapp/", include("apps.whatsapp.urls")),
    # Statistics
    path("estatisticas/", include("apps.estatisticas.urls")),
    # Root redirect to dashboard
    path("", RedirectView.as_view(pattern_name="dashboard:home", permanent=False)),
]

# API Documentation
if settings.DEBUG:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
        SpectacularRedocView,
    )

    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
        ),
    ]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
