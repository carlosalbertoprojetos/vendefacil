"""
URLs for API v1.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProdutoViewSet, CategoriaViewSet, PedidoViewSet,
    UserViewSet, EmpresaViewSet
)

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'usuarios', UserViewSet)
router.register(r'empresas', EmpresaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
