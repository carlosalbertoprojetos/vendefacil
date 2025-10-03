"""
Views for catalogo app.
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from apps.produtos.models import Produto
from apps.authentication.models import User, Empresa


def catalogo_list(request):
    """Lista catálogo geral"""
    from apps.produtos.models import Categoria

    produtos = (
        Produto.active_objects.filter(disponivel=True)
        .select_related("categoria", "subcategoria")
        .prefetch_related("imagens")
    )

    # Filtros
    categoria = request.GET.get("categoria")
    if categoria:
        produtos = produtos.filter(categoria_id=categoria)

    # Ordenação
    ordenacao = request.GET.get("ordenacao", "nome")
    if ordenacao == "preco_menor":
        produtos = produtos.order_by("preco")
    elif ordenacao == "preco_maior":
        produtos = produtos.order_by("-preco")
    elif ordenacao == "nome":
        produtos = produtos.order_by("nome")
    elif ordenacao == "destaque":
        produtos = produtos.order_by("-em_destaque", "nome")

    # Paginação
    paginator = Paginator(produtos, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "object_list": page_obj,
        "categorias": Categoria.active_objects.all(),
        "categoria_atual": categoria,
        "ordenacao_atual": ordenacao,
    }

    return render(request, "catalogo/list.html", context)


def catalogo_vendedor(request, vendedor_id):
    """Catálogo de um vendedor específico"""
    vendedor = get_object_or_404(User, id=vendedor_id, role="VENDEDOR")
    produtos = Produto.active_objects.filter(vendedor=vendedor, disponivel=True)

    # Paginação
    paginator = Paginator(produtos, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "vendedor": vendedor,
        "produtos": page_obj,
    }

    return render(request, "catalogo/vendedor.html", context)


def catalogo_empresa(request, empresa_id):
    """Catálogo de uma empresa específica"""
    empresa = get_object_or_404(Empresa, id=empresa_id)
    produtos = Produto.active_objects.filter(
        vendedor__profile__empresa=empresa, disponivel=True
    )

    # Paginação
    paginator = Paginator(produtos, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "empresa": empresa,
        "produtos": page_obj,
    }

    return render(request, "catalogo/empresa.html", context)
