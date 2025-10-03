"""
Views for notificacoes app.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def notifications_home(request):
    """Página inicial de notificações"""
    return render(request, 'notificacoes/home.html')


@login_required
def send_notification(request):
    """Envia notificação"""
    if request.method == 'POST':
        # Aqui você implementaria a lógica de envio de notificação
        pass
    
    return render(request, 'notificacoes/send.html')
