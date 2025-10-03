"""
Decorators for dashboard app.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


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
