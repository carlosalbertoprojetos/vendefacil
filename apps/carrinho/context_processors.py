"""
Context processors for carrinho app.
"""

from .cart import Cart


def carrinho(request):
    """Adiciona carrinho ao contexto"""
    return {
        'carrinho': Cart(request)
    }
