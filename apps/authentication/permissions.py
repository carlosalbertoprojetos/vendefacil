"""
Permission system for VendaSimples project.
"""

from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied


# Permissões por função
ROLE_PERMISSIONS = {
    "SUPER": [
        "view_all_users",
        "manage_all_empresas",
        "manage_all_vendedores",
        "view_all_produtos",
        "manage_all_produtos",
        "view_all_pedidos",
        "manage_all_pedidos",
        "view_statistics",
        "manage_system_settings",
    ],
    "EMPRESA": [
        "view_own_empresa",
        "manage_own_empresa",
        "view_own_vendedores",
        "manage_own_vendedores",
        "view_own_produtos",
        "manage_own_produtos",
        "view_own_pedidos",
        "manage_own_pedidos",
        "view_own_statistics",
        "manage_own_settings",
    ],
    "VENDEDOR": [
        "view_own_profile",
        "manage_own_profile",
        "view_own_produtos",
        "manage_own_produtos",
        "view_own_pedidos",
        "manage_own_pedidos",
        "view_own_statistics",
    ],
}


class RoleRequiredMixin:
    """Mixin para verificar função do usuário"""

    required_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.role not in self.required_roles:
            raise PermissionDenied("Você não tem permissão para acessar esta página.")

        return super().dispatch(request, *args, **kwargs)


class SuperUserRequiredMixin(RoleRequiredMixin):
    """Mixin para superusuários"""

    required_roles = ["SUPER"]


class EmpresaRequiredMixin(RoleRequiredMixin):
    """Mixin para empresas"""

    required_roles = ["SUPER", "EMPRESA"]


class VendedorRequiredMixin(RoleRequiredMixin):
    """Mixin para vendedores"""

    required_roles = ["SUPER", "EMPRESA", "VENDEDOR"]


def role_required(roles):
    """Decorator para verificar função"""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login

                return redirect_to_login(request.get_full_path())

            if request.user.role not in roles:
                raise PermissionDenied(
                    "Você não tem permissão para acessar esta página."
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


class EmailBackend(ModelBackend):
    """Backend de autenticação por email"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.get_user_model().objects.get(email__iexact=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except self.get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.get_user_model().objects.get(pk=user_id)
        except self.get_user_model().DoesNotExist:
            return None
