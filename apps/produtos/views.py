"""
Views for produtos app.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Produto, Categoria, Subcategoria
from .forms import ProdutoForm


@login_required
def produto_list(request):
    """Lista produtos do usuário"""
    produtos = Produto.active_objects.filter(vendedor=request.user)

    # Filtros
    categoria = request.GET.get("categoria")
    if categoria:
        produtos = produtos.filter(categoria_id=categoria)

    # Paginação
    paginator = Paginator(produtos, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "object_list": page_obj,
        "categorias": Categoria.active_objects.all(),
    }

    return render(request, "produtos/list.html", context)


@login_required
def produto_create(request):
    """Cria novo produto"""
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                produto = form.save(commit=False)
                produto.vendedor = request.user
                produto.save()
                messages.success(request, "Produto criado com sucesso!")
                return redirect("produtos:detail", pk=produto.pk)
            except Exception as e:
                print(f"Erro ao salvar produto: {e}")
                messages.error(request, f"Erro ao salvar produto: {e}")
        else:
            # Debug: mostrar erros do formulário
            print("Erros do formulário:", form.errors)
            for field, errors in form.errors.items():
                print(f"Campo {field}: {errors}")
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = ProdutoForm()

    context = {
        "form": form,
    }

    return render(request, "produtos/create.html", context)


@login_required
def produto_detail(request, pk):
    """Detalhes do produto"""
    produto = get_object_or_404(Produto, pk=pk)

    # Verifica permissão
    if not request.user.can_manage_produto(produto):
        messages.error(request, "Você não tem permissão para ver este produto.")
        return redirect("produtos:list")

    # Incrementa visualização
    produto.incrementar_visualizacao()

    # Breadcrumbs
    breadcrumbs = [
        ("Dashboard", "/dashboard/"),
        ("Produtos", "/produtos/"),
        (produto.nome, None),
    ]

    context = {
        "object": produto,
        "breadcrumbs": breadcrumbs,
    }

    return render(request, "produtos/detail.html", context)


@login_required
def produto_edit(request, pk):
    """Edita produto"""
    produto = get_object_or_404(Produto, pk=pk)

    # Verifica permissão
    if not request.user.can_manage_produto(produto):
        messages.error(request, "Você não tem permissão para editar este produto.")
        return redirect("produtos:list")

    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("produtos:detail", pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)

    context = {
        "form": form,
        "produto": produto,
    }

    return render(request, "produtos/edit.html", context)


@login_required
def produto_delete(request, pk):
    """Deleta produto"""
    produto = get_object_or_404(Produto, pk=pk)

    # Verifica permissão
    if not request.user.can_manage_produto(produto):
        messages.error(request, "Você não tem permissão para deletar este produto.")
        return redirect("produtos:list")

    if request.method == "POST":
        produto.delete()
        messages.success(request, "Produto excluído com sucesso!")
        return redirect("produtos:list")

    context = {
        "produto": produto,
    }

    return render(request, "produtos/delete.html", context)


def categoria_list(request):
    """Lista categorias"""
    categorias = Categoria.active_objects.all()

    context = {
        "categorias": categorias,
    }

    return render(request, "produtos/categorias.html", context)


@require_http_methods(["GET"])
def get_subcategorias(request):
    """View AJAX para buscar subcategorias de uma categoria"""
    categoria_id = request.GET.get("categoria_id")

    if not categoria_id:
        return JsonResponse({"subcategorias": []})

    try:
        subcategorias = Subcategoria.objects.filter(
            categoria_id=categoria_id, is_active=True
        ).order_by("nome")

        data = {
            "subcategorias": [{"id": sub.id, "nome": sub.nome} for sub in subcategorias]
        }

        return JsonResponse(data)

    except (ValueError, Subcategoria.DoesNotExist):
        return JsonResponse({"subcategorias": []})
