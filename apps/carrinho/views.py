"""
Views for carrinho app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .cart import Cart
from apps.produtos.models import Produto


def cart_detail(request):
    """Visualiza o carrinho"""
    cart = Cart(request)
    return render(request, "carrinho/cart.html", {"cart": cart})


@require_POST
def cart_add(request, produto_id):
    """Adiciona produto ao carrinho"""
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = int(request.POST.get("quantidade", 1))
    variacao = request.POST.get("variacao", "")

    cart.add(produto, quantidade, variacao)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "message": "Produto adicionado ao carrinho",
                "cart_total": len(cart),
                "cart_price": str(cart.get_total_price()),
            }
        )

    return redirect("carrinho:detail")


@require_POST
def cart_remove(request, produto_id):
    """Remove produto do carrinho"""
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=produto_id)
    variacao = request.POST.get("variacao", "")

    cart.remove(produto, variacao)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "message": "Produto removido do carrinho",
                "cart_total": len(cart),
                "cart_price": str(cart.get_total_price()),
            }
        )

    return redirect("carrinho:detail")


@require_POST
def cart_update(request, produto_id):
    """Atualiza quantidade do produto"""
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = int(request.POST.get("quantidade", 1))
    variacao = request.POST.get("variacao", "")

    cart.update(produto, quantidade, variacao)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "success": True,
                "message": "Carrinho atualizado",
                "cart_total": len(cart),
                "cart_price": str(cart.get_total_price()),
            }
        )

    return redirect("carrinho:detail")


@require_POST
def cart_clear(request):
    """Limpa o carrinho"""
    cart = Cart(request)
    cart.clear()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True, "message": "Carrinho limpo"})

    return redirect("carrinho:detail")


@require_POST
def cart_remove_ajax(request):
    """Remove produto do carrinho via AJAX"""
    cart = Cart(request)
    import json

    data = json.loads(request.body) if request.body else {}
    produto_id = data.get("product_id")

    if not produto_id:
        return JsonResponse(
            {"success": False, "message": "ID do produto não fornecido"}, status=400
        )

    try:
        produto = get_object_or_404(Produto, id=produto_id)
        cart.remove(produto)

        return JsonResponse(
            {
                "success": True,
                "message": "Produto removido do carrinho",
                "cart_total": len(cart),
                "cart_price": str(cart.get_total_price()),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@require_POST
def cart_update_ajax(request):
    """Atualiza quantidade do produto via AJAX"""
    cart = Cart(request)
    import json

    data = json.loads(request.body) if request.body else {}
    produto_id = data.get("product_id")
    quantidade = data.get("quantity", 1)

    if not produto_id:
        return JsonResponse(
            {"success": False, "message": "ID do produto não fornecido"}, status=400
        )

    try:
        produto = get_object_or_404(Produto, id=produto_id)
        cart.update(produto, quantidade)

        return JsonResponse(
            {
                "success": True,
                "message": "Carrinho atualizado",
                "cart_total": len(cart),
                "cart_price": str(cart.get_total_price()),
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
