"""
Views for pagamento app.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from apps.carrinho.cart import Cart
from apps.pedidos.models import Pedido, ItemPedido, StatusPedido
from apps.produtos.models import Produto


@login_required
def payment_home(request):
    """Página inicial de pagamentos"""
    return render(request, "pagamento/home.html")


@login_required
def process_payment(request):
    """Processa pagamento"""
    if request.method == "POST":
        # Aqui você implementaria a lógica de processamento de pagamento
        pass

    return render(request, "pagamento/process.html")


def payment_success(request):
    """Pagamento realizado com sucesso"""
    return render(request, "pagamento/success.html")


def payment_failure(request):
    """Falha no pagamento"""
    return render(request, "pagamento/failure.html")


@login_required
def checkout(request):
    """Página de checkout"""
    cart = Cart(request)

    if not cart:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect("carrinho:detail")

    if request.method == "POST":
        # Processar pedido
        try:
            with transaction.atomic():
                # Coletar dados do formulário
                metodo_pagamento = request.POST.get("metodo_pagamento")
                if not metodo_pagamento or metodo_pagamento not in [
                    "pix",
                    "cartao",
                    "boleto",
                ]:
                    metodo_pagamento = "pix"  # Valor padrão

                dados_cliente = {
                    "nome": request.POST.get("nome"),
                    "email": request.POST.get("email"),
                    "telefone": request.POST.get("telefone"),
                    "cep": request.POST.get("cep"),
                    "endereco": request.POST.get("endereco"),
                    "numero": request.POST.get("numero"),
                    "bairro": request.POST.get("bairro"),
                    "cidade": request.POST.get("cidade"),
                    "estado": request.POST.get("estado"),
                    "metodo_pagamento": metodo_pagamento,
                }

                # Gerar número do pedido
                numero_pedido = f"PED{timezone.now().strftime('%Y%m%d%H%M%S')}"

                # Criar pedido
                pedido = Pedido.objects.create(
                    numero=numero_pedido,
                    vendedor=request.user,  # Assumindo que o usuário logado é o vendedor
                    cliente_nome=dados_cliente["nome"],
                    cliente_telefone=dados_cliente["telefone"],
                    cliente_email=dados_cliente["email"],
                    endereco_cep=dados_cliente["cep"],
                    endereco_logradouro=dados_cliente["endereco"],
                    endereco_numero=dados_cliente["numero"],
                    endereco_bairro=dados_cliente["bairro"],
                    endereco_cidade=dados_cliente["cidade"],
                    endereco_estado=dados_cliente["estado"],
                    status=StatusPedido.PENDENTE,
                    subtotal=cart.get_total_price(),
                    frete=0,  # Frete grátis por enquanto
                    total=cart.get_total_price(),
                    observacoes=f"Método de pagamento: {dados_cliente['metodo_pagamento'].upper()}",
                )

                # Criar itens do pedido
                for item in cart:
                    ItemPedido.objects.create(
                        pedido=pedido,
                        produto=item["produto"],
                        quantidade=item["quantidade"],
                        preco_unitario=item["preco"],
                        preco_total=item["total"],
                    )

                # Limpar carrinho após processamento
                cart.clear()

                # Mostrar mensagem de sucesso
                messages.success(
                    request,
                    f"Pedido #{numero_pedido} realizado com sucesso! Você receberá um e-mail de confirmação.",
                )

                # Redirecionar para página de sucesso
                return redirect("pagamento:success")

        except Exception as e:
            messages.error(request, f"Erro ao processar pedido: {str(e)}")
            return redirect("pagamento:checkout")

    context = {
        "cart": cart,
        "total": cart.get_total_price(),
    }

    return render(request, "pagamento/checkout.html", context)
