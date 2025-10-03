"""
Models for whatsapp app.
"""

from django.db import models
from django.conf import settings


class WhatsAppSettings(models.Model):
    """Configurações de WhatsApp por usuário"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="whatsapp_settings",
        verbose_name="Usuário",
    )
    numero_whatsapp = models.CharField(
        max_length=30, blank=True, verbose_name="Número do WhatsApp"
    )
    nome_empresa = models.CharField(
        max_length=255, blank=True, verbose_name="Nome da Empresa"
    )
    mensagem_pedido = models.TextField(blank=True, verbose_name="Mensagem de Pedido")
    mensagem_entrega = models.TextField(blank=True, verbose_name="Mensagem de Entrega")
    enviar_pedido = models.BooleanField(default=True, verbose_name="Enviar ao criar pedido")
    enviar_entrega = models.BooleanField(default=True, verbose_name="Enviar ao despachar pedido")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "whatsapp_settings"
        verbose_name = "Configuração de WhatsApp"
        verbose_name_plural = "Configurações de WhatsApp"

    def __str__(self):
        return f"WhatsAppSettings de {self.user.get_full_name() or self.user.email}"


