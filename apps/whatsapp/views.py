"""
Views for whatsapp app.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def whatsapp_home(request):
    """Página inicial do WhatsApp"""
    return render(request, 'whatsapp/home.html')


@login_required
def send_message(request):
    """Envia mensagem via WhatsApp"""
    if request.method == 'POST':
        # Aqui você implementaria a lógica de envio de mensagem
        pass
    
    return render(request, 'whatsapp/send.html')


def webhook(request):
    """Webhook para receber mensagens do WhatsApp"""
    if request.method == 'POST':
        # Aqui você implementaria a lógica do webhook
        pass
    
    return render(request, 'whatsapp/webhook.html')
