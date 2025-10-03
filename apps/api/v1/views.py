"""
Views for API v1.
"""

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.produtos.models import Produto, Categoria
from apps.pedidos.models import Pedido
from apps.authentication.models import User, Empresa
from .serializers import (
    ProdutoSerializer, CategoriaSerializer, PedidoSerializer,
    UserSerializer, EmpresaSerializer
)


class ProdutoViewSet(viewsets.ModelViewSet):
    """ViewSet para Produto"""
    queryset = Produto.active_objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def destacados(self, request):
        """Retorna produtos em destaque"""
        produtos = self.queryset.filter(em_destaque=True)
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)


class CategoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para Categoria"""
    queryset = Categoria.active_objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PedidoViewSet(viewsets.ModelViewSet):
    """ViewSet para Pedido"""
    queryset = Pedido.active_objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtra pedidos baseado no usuário"""
        if self.request.user.role == 'SUPER':
            return self.queryset
        elif self.request.user.role == 'EMPRESA':
            return self.queryset.filter(
                vendedor__profile__empresa=self.request.user.empresa
            )
        else:
            return self.queryset.filter(vendedor=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para User"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmpresaViewSet(viewsets.ModelViewSet):
    """ViewSet para Empresa"""
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated]
