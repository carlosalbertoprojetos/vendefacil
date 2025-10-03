"""
Views for pedidos app.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Pedido, StatusPedido


@login_required
def pedido_list(request):
    """Lista pedidos do usuário"""
    if request.user.role == "SUPERUSER":
        pedidos = Pedido.active_objects.all()
    elif request.user.role == "EMPRESA":
        pedidos = Pedido.active_objects.filter(
            vendedor__profile__empresa=request.user.profile.empresa
        )
    else:
        pedidos = Pedido.active_objects.filter(vendedor=request.user)

    # Filtros
    status = request.GET.get("status")
    if status:
        pedidos = pedidos.filter(status=status)

    # Paginação
    paginator = Paginator(pedidos, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "object_list": page_obj,
        "status_list": StatusPedido.choices,
    }

    return render(request, "pedidos/list.html", context)


@login_required
def pedido_detail(request, pk):
    """Detalhes do pedido"""
    pedido = get_object_or_404(Pedido, pk=pk)

    # Verifica permissão
    if not request.user.can_view_pedido(pedido):
        messages.error(request, "Você não tem permissão para ver este pedido.")
        return redirect("pedidos:list")

    context = {
        "pedido": pedido,
        "status_choices": StatusPedido.choices,
    }

    return render(request, "pedidos/detail.html", context)


@login_required
def pedido_status_update(request, pk):
    """Atualiza status do pedido"""
    pedido = get_object_or_404(Pedido, pk=pk)

    # Verifica permissão
    if not request.user.can_view_pedido(pedido):
        messages.error(request, "Você não tem permissão para atualizar este pedido.")
        return redirect("pedidos:list")

    if request.method == "POST":
        novo_status = request.POST.get("status")
        if novo_status in dict(StatusPedido.choices):
            status_anterior = pedido.status
            pedido.status = novo_status
            pedido.save()

            # Cria histórico
            pedido.historico_status.create(
                status_anterior=status_anterior,
                status_novo=novo_status,
                usuario=request.user,
                observacoes=request.POST.get("observacoes", ""),
            )

            messages.success(request, "Status do pedido atualizado!")

        return redirect("pedidos:detail", pk=pedido.pk)

    context = {
        "pedido": pedido,
        "status_choices": StatusPedido.choices,
    }

    return render(request, "pedidos/status_update.html", context)


@login_required
def pedido_edit(request, pk):
    """Edita pedido existente"""
    pedido = get_object_or_404(Pedido, pk=pk)

    # Verifica permissão
    if not request.user.can_view_pedido(pedido):
        messages.error(request, "Você não tem permissão para editar este pedido.")
        return redirect("pedidos:list")

    if request.method == "POST":
        # Atualiza dados do cliente
        pedido.cliente_nome = request.POST.get("cliente_nome", pedido.cliente_nome)
        pedido.cliente_telefone = request.POST.get(
            "cliente_telefone", pedido.cliente_telefone
        )
        pedido.cliente_email = request.POST.get("cliente_email", pedido.cliente_email)
        pedido.cliente_cpf = request.POST.get("cliente_cpf", pedido.cliente_cpf)

        # Atualiza endereço
        pedido.endereco_cep = request.POST.get("endereco_cep", pedido.endereco_cep)
        pedido.endereco_logradouro = request.POST.get(
            "endereco_logradouro", pedido.endereco_logradouro
        )
        pedido.endereco_numero = request.POST.get(
            "endereco_numero", pedido.endereco_numero
        )
        pedido.endereco_complemento = request.POST.get(
            "endereco_complemento", pedido.endereco_complemento
        )
        pedido.endereco_bairro = request.POST.get(
            "endereco_bairro", pedido.endereco_bairro
        )
        pedido.endereco_cidade = request.POST.get(
            "endereco_cidade", pedido.endereco_cidade
        )
        pedido.endereco_estado = request.POST.get(
            "endereco_estado", pedido.endereco_estado
        )

        # Atualiza observações
        pedido.observacoes = request.POST.get("observacoes", pedido.observacoes)

        # Atualiza data de entrega prevista
        data_entrega = request.POST.get("data_entrega_prevista")
        if data_entrega:
            from django.utils.dateparse import parse_datetime

            pedido.data_entrega_prevista = parse_datetime(data_entrega)

        # Atualiza status se fornecido
        novo_status = request.POST.get("status")
        if novo_status and novo_status in dict(StatusPedido.choices):
            status_anterior = pedido.status
            if status_anterior != novo_status:
                pedido.status = novo_status
                # Cria histórico de mudança de status
                pedido.historico_status.create(
                    status_anterior=status_anterior,
                    status_novo=novo_status,
                    usuario=request.user,
                    observacoes=request.POST.get("status_observacoes", ""),
                )

        pedido.save()
        messages.success(request, "Pedido atualizado com sucesso!")
        return redirect("pedidos:detail", pk=pedido.pk)

    context = {
        "pedido": pedido,
        "status_choices": StatusPedido.choices,
    }

    return render(request, "pedidos/edit.html", context)


@login_required
def pedido_create(request):
    """Cria novo pedido"""
    if request.method == "POST":
        # Aqui você implementaria a lógica de criação do pedido
        # Por enquanto, apenas redireciona
        messages.success(request, "Pedido criado com sucesso!")
        return redirect("pedidos:list")

    return render(request, "pedidos/create.html")
