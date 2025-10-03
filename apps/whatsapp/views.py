"""
Views for whatsapp app.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WhatsAppSettings


@login_required
def whatsapp_home(request):
    """Página inicial do WhatsApp"""
    user = request.user

    # Carregar ou criar configurações do usuário
    settings_obj, created = WhatsAppSettings.objects.get_or_create(user=user)

    # Mensagens padrão
    default_mensagem_pedido = (
        "Olá! Seu pedido foi realizado com sucesso! 🎉\n\n"
        "📦 Pedido: #{{pedido_numero}}\n"
        "💰 Total: R$ {{pedido_total}}\n"
        "📅 Data: {{pedido_data}}\n\n"
        "Acompanhe seu pedido em tempo real e receba atualizações automáticas.\n\n"
        "Obrigado por escolher a nossa loja! 🛍️"
    )
    default_mensagem_entrega = (
        "🚚 Seu pedido está a caminho!\n\n"
        "📦 Pedido: #{{pedido_numero}}\n"
        "🚛 Código de rastreamento: {{codigo_rastreamento}}\n"
        "📅 Previsão de entrega: {{previsao_entrega}}\n\n"
        "Acompanhe seu pedido: {{link_rastreamento}}\n\n"
        "Obrigado pela preferência! 🎉"
    )

    # Preencher mensagens padrão uma única vez, quando estiverem em branco
    to_save = False
    if not settings_obj.mensagem_pedido:
        settings_obj.mensagem_pedido = default_mensagem_pedido
        to_save = True
    if not settings_obj.mensagem_entrega:
        settings_obj.mensagem_entrega = default_mensagem_entrega
        to_save = True
    if to_save:
        settings_obj.save()

    if request.method == "POST":
        settings_obj.numero_whatsapp = request.POST.get(
            "numero_whatsapp", settings_obj.numero_whatsapp
        )
        settings_obj.nome_empresa = request.POST.get(
            "nome_empresa", settings_obj.nome_empresa
        )
        settings_obj.mensagem_pedido = request.POST.get(
            "mensagem_pedido", settings_obj.mensagem_pedido
        )
        settings_obj.mensagem_entrega = request.POST.get(
            "mensagem_entrega", settings_obj.mensagem_entrega
        )
        settings_obj.enviar_pedido = request.POST.get("enviar_pedido") == "on"
        settings_obj.enviar_entrega = request.POST.get("enviar_entrega") == "on"
        settings_obj.save()

        messages.success(request, "Configurações do WhatsApp salvas com sucesso!")
        return redirect("whatsapp:home")

    context = {
        "settings": settings_obj,
    }
    return render(request, "whatsapp/home.html", context)


@login_required
def send_message(request):
    """Envia mensagem via WhatsApp"""
    if request.method == "POST":
        # Aqui você implementaria a lógica de envio de mensagem
        pass

    return render(request, "whatsapp/send.html")


def webhook(request):
    """Webhook para receber mensagens do WhatsApp"""
    if request.method == "POST":
        # Aqui você implementaria a lógica do webhook
        pass

    return render(request, "whatsapp/webhook.html")
