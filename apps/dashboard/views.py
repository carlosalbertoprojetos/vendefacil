"""
Views for dashboard app.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import role_required


@login_required
def home(request):
    """Dashboard principal"""
    from apps.authentication.models import UserRole
    from django.db.models import Count, Sum
    from django.utils import timezone
    from datetime import timedelta

    user = request.user
    context = {"user": user}

    # Redireciona baseado no papel do usuário
    if user.role == UserRole.SUPERUSER:
        # Dashboard do administrador
        from apps.authentication.models import User
        from apps.produtos.models import Produto
        from apps.pedidos.models import Pedido, StatusPedido

        # Estatísticas gerais
        total_usuarios = User.objects.count()
        total_produtos = Produto.objects.count()
        total_pedidos = Pedido.objects.count()

        # Pedidos por status
        pedidos_por_status = (
            Pedido.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )

        # Vendas dos últimos 30 dias
        data_30_dias_atras = timezone.now() - timedelta(days=30)
        vendas_30_dias = (
            Pedido.objects.filter(
                created_at__gte=data_30_dias_atras,
                status__in=[StatusPedido.CONFIRMADO, StatusPedido.ENTREGUE],
            ).aggregate(total=Sum("total"))["total"]
            or 0
        )

        # Pedidos recentes
        pedidos_recentes = Pedido.objects.select_related("vendedor").order_by(
            "-created_at"
        )[:5]

        context.update(
            {
                "total_usuarios": total_usuarios,
                "total_produtos": total_produtos,
                "total_pedidos": total_pedidos,
                "pedidos_por_status": pedidos_por_status,
                "vendas_30_dias": vendas_30_dias,
                "pedidos_recentes": pedidos_recentes,
            }
        )

        return render(request, "dashboard/admin.html", context)

    elif user.role == UserRole.EMPRESA:
        # Dashboard da empresa
        from apps.produtos.models import Produto
        from apps.pedidos.models import Pedido, StatusPedido

        # Produtos da empresa
        total_produtos = Produto.objects.filter(
            vendedor__profile__empresa=user.profile.empresa
        ).count()

        # Pedidos da empresa
        pedidos_empresa = Pedido.objects.filter(
            vendedor__profile__empresa=user.profile.empresa
        )
        total_pedidos = pedidos_empresa.count()

        # Vendas dos últimos 30 dias
        data_30_dias_atras = timezone.now() - timedelta(days=30)
        vendas_30_dias = (
            pedidos_empresa.filter(
                created_at__gte=data_30_dias_atras,
                status__in=[StatusPedido.CONFIRMADO, StatusPedido.ENTREGUE],
            ).aggregate(total=Sum("total"))["total"]
            or 0
        )

        # Pedidos por status
        pedidos_por_status = (
            pedidos_empresa.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )

        # Vendedores da empresa
        vendedores = (
            user.profile.empresa.vendedores.all()
            if hasattr(user.profile.empresa, "vendedores")
            else []
        )

        context.update(
            {
                "empresa": user.profile.empresa,
                "total_produtos": total_produtos,
                "total_pedidos": total_pedidos,
                "vendas_30_dias": vendas_30_dias,
                "pedidos_por_status": pedidos_por_status,
                "vendedores": vendedores,
            }
        )

        return render(request, "dashboard/empresa.html", context)

    else:
        # Dashboard do vendedor
        from apps.produtos.models import Produto
        from apps.pedidos.models import Pedido, StatusPedido

        # Produtos do vendedor
        total_produtos = Produto.objects.filter(vendedor=user).count()

        # Pedidos do vendedor
        pedidos_vendedor = Pedido.objects.filter(vendedor=user)
        total_pedidos = pedidos_vendedor.count()

        # Vendas dos últimos 30 dias
        data_30_dias_atras = timezone.now() - timedelta(days=30)
        vendas_30_dias = (
            pedidos_vendedor.filter(
                created_at__gte=data_30_dias_atras,
                status__in=[StatusPedido.CONFIRMADO, StatusPedido.ENTREGUE],
            ).aggregate(total=Sum("total"))["total"]
            or 0
        )

        # Pedidos por status
        pedidos_por_status = (
            pedidos_vendedor.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )

        # Pedidos recentes
        pedidos_recentes = pedidos_vendedor.order_by("-created_at")[:5]

        # Produtos com baixo estoque
        produtos_baixo_estoque = Produto.objects.filter(
            vendedor=user, estoque__lte=5
        ).order_by("estoque")[:5]

        context.update(
            {
                "total_produtos": total_produtos,
                "total_pedidos": total_pedidos,
                "vendas_30_dias": vendas_30_dias,
                "pedidos_por_status": pedidos_por_status,
                "pedidos_recentes": pedidos_recentes,
                "produtos_baixo_estoque": produtos_baixo_estoque,
            }
        )

        return render(request, "dashboard/vendedor.html", context)


@role_required(["SUPERUSER", "EMPRESA"])
@login_required
def empresa_dashboard(request):
    """Dashboard da empresa"""
    from apps.authentication.models import UserRole

    user = request.user
    empresa = getattr(user, "empresa", None)

    context = {
        "user": user,
        "empresa": empresa,
        "total_vendedores": getattr(empresa, "total_vendedores", 0) if empresa else 0,
        "total_produtos": getattr(empresa, "total_produtos", 0) if empresa else 0,
    }

    return render(request, "dashboard/empresa.html", context)


@role_required(["SUPERUSER", "EMPRESA", "VENDEDOR"])
@login_required
def vendedor_dashboard(request):
    """Dashboard do vendedor"""
    user = request.user

    context = {
        "user": user,
        "total_produtos": (
            getattr(user, "produtos", []).count() if hasattr(user, "produtos") else 0
        ),
        "total_pedidos": (
            getattr(user, "pedidos_vendedor", []).count()
            if hasattr(user, "pedidos_vendedor")
            else 0
        ),
    }

    return render(request, "dashboard/vendedor.html", context)


@role_required(["SUPERUSER"])
@login_required
def admin_dashboard(request):
    """Dashboard do administrador"""
    from apps.authentication.models import User

    # Tentar importar os modelos, se não existirem, usar valores padrão
    try:
        from apps.produtos.models import Produto

        total_produtos = Produto.objects.count()
    except ImportError:
        total_produtos = 0

    try:
        from apps.pedidos.models import Pedido

        total_pedidos = Pedido.objects.count()
    except ImportError:
        total_pedidos = 0

    context = {
        "total_usuarios": User.objects.count(),
        "total_produtos": total_produtos,
        "total_pedidos": total_pedidos,
    }

    return render(request, "dashboard/admin.html", context)
