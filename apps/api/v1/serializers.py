"""
Serializers for API v1.
"""

from rest_framework import serializers
from apps.produtos.models import Produto, Categoria
from apps.pedidos.models import Pedido
from apps.authentication.models import User, Empresa


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para Categoria"""
    
    class Meta:
        model = Categoria
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    """Serializer para Produto"""
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Produto
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    """Serializer para Pedido"""
    
    class Meta:
        model = Pedido
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Serializer para User"""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para Empresa"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Empresa
        fields = '__all__'
