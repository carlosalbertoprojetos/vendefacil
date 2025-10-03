"""
Decorators for authentication app.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def role_required(roles):
    """Decorator para verificar função do usuário"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Você precisa estar logado para acessar esta página.')
                return redirect('authentication:login')
            
            if request.user.role not in roles:
                messages.error(request, 'Você não tem permissão para acessar esta página.')
                return redirect('dashboard:home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def superuser_required(view_func):
    """Decorator para superusuários"""
    return role_required(['SUPER'])(view_func)


def empresa_required(view_func):
    """Decorator para empresas"""
    return role_required(['SUPER', 'EMPRESA'])(view_func)


def vendedor_required(view_func):
    """Decorator para vendedores"""
    return role_required(['SUPER', 'EMPRESA', 'VENDEDOR'])(view_func)


def verified_user_required(view_func):
    """Decorator para usuários verificados"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('authentication:login')
        
        if not request.user.is_verified:
            messages.warning(request, 'Você precisa verificar seu email para acessar esta página.')
            return redirect('authentication:verify_email')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def ajax_required(view_func):
    """Decorator para views que requerem AJAX"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Esta view requer AJAX'}, status=400)
        return view_func(request, *args, **kwargs)
    return wrapper
