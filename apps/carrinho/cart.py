"""
Cart functionality for VendaSimples project.
"""

from decimal import Decimal
from django.conf import settings


class Cart:
    """Classe principal do carrinho de compras"""

    def __init__(self, request):
        """Inicializa o carrinho"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, produto, quantidade=1, variacao=None):
        """Adiciona produto ao carrinho"""
        produto_id = str(produto.id)
        variacao_key = variacao or ""
        cart_key = f"{produto_id}_{variacao_key}"

        if cart_key in self.cart:
            self.cart[cart_key]["quantidade"] += quantidade
        else:
            self.cart[cart_key] = {
                "produto_id": produto_id,
                "nome": produto.nome,
                "preco": str(produto.preco_final),
                "quantidade": quantidade,
                "variacao": variacao_key,
                "imagem": (
                    produto.imagem_principal.imagem.url
                    if produto.imagem_principal and produto.imagem_principal.imagem
                    else ""
                ),
            }

        self.save()

    def remove(self, produto, variacao=None):
        """Remove produto do carrinho"""
        produto_id = str(produto.id)
        variacao_key = variacao or ""
        cart_key = f"{produto_id}_{variacao_key}"

        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def update(self, produto, quantidade, variacao=None):
        """Atualiza quantidade do produto"""
        produto_id = str(produto.id)
        variacao_key = variacao or ""
        cart_key = f"{produto_id}_{variacao_key}"

        if cart_key in self.cart:
            if quantidade <= 0:
                self.remove(produto, variacao)
            else:
                self.cart[cart_key]["quantidade"] = quantidade
                self.save()

    def clear(self):
        """Limpa o carrinho"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def save(self):
        """Salva o carrinho na sessão"""
        self.session.modified = True

    def __iter__(self):
        """Itera sobre os itens do carrinho"""
        produto_ids = []
        for item in self.cart.values():
            produto_ids.append(item["produto_id"])

        from apps.produtos.models import Produto

        produtos = Produto.active_objects.filter(id__in=produto_ids)
        produto_dict = {produto.id: produto for produto in produtos}

        for item in self.cart.values():
            produto = produto_dict.get(int(item["produto_id"]))
            if produto:
                item["produto"] = produto
                item["preco"] = Decimal(item["preco"])
                item["total"] = item["preco"] * item["quantidade"]

                # Calcular desconto total se houver promoção
                if produto.preco_promocional and produto.em_promocao:
                    preco_original = produto.preco
                    preco_promocional = item["preco"]
                    desconto_unitario = preco_original - preco_promocional
                    item["desconto_total"] = desconto_unitario * item["quantidade"]
                else:
                    item["desconto_total"] = Decimal("0")

                yield item

    def __len__(self):
        """Retorna quantidade total de itens"""
        return sum(item["quantidade"] for item in self.cart.values())

    def get_total_price(self):
        """Retorna preço total do carrinho"""
        return sum(
            Decimal(item["preco"]) * item["quantidade"] for item in self.cart.values()
        )

    def get_total_items(self):
        """Retorna quantidade total de itens"""
        return sum(item["quantidade"] for item in self.cart.values())

    def is_empty(self):
        """Verifica se carrinho está vazio"""
        return len(self.cart) == 0
