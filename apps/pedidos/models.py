"""
Order models for VendaSimples project.
"""

from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel, SoftDeleteModel
from apps.core.managers import ActiveSoftDeleteManager


class StatusPedido(models.TextChoices):
    PENDENTE = 'PENDENTE', 'Pendente'
    CONFIRMADO = 'CONFIRMADO', 'Confirmado'
    PREPARANDO = 'PREPARANDO', 'Preparando'
    PRONTO = 'PRONTO', 'Pronto para Entrega'
    SAIU_ENTREGA = 'SAIU_ENTREGA', 'Saiu para Entrega'
    ENTREGUE = 'ENTREGUE', 'Entregue'
    CANCELADO = 'CANCELADO', 'Cancelado'


class Pedido(TimeStampedModel, SoftDeleteModel):
    """Modelo de pedido"""
    # Identificação
    numero = models.CharField(
        max_length=20, 
        unique=True, 
        db_index=True,
        verbose_name='Número do Pedido'
    )
    
    # Relacionamentos
    vendedor = models.ForeignKey(
        'authentication.User',
        on_delete=models.PROTECT,
        related_name='pedidos_vendedor',
        verbose_name='Vendedor'
    )
    cliente_usuario = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos_cliente',
        verbose_name='Cliente (Usuário)'
    )
    
    # Dados do Cliente
    cliente_nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Cliente'
    )
    cliente_telefone = models.CharField(
        max_length=20,
        verbose_name='Telefone do Cliente'
    )
    cliente_email = models.EmailField(
        blank=True,
        verbose_name='E-mail do Cliente'
    )
    cliente_cpf = models.CharField(
        max_length=14, 
        blank=True,
        verbose_name='CPF do Cliente'
    )
    
    # Endereço de Entrega
    endereco_cep = models.CharField(
        max_length=9,
        verbose_name='CEP'
    )
    endereco_logradouro = models.CharField(
        max_length=255,
        verbose_name='Logradouro'
    )
    endereco_numero = models.CharField(
        max_length=20,
        verbose_name='Número'
    )
    endereco_complemento = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='Complemento'
    )
    endereco_bairro = models.CharField(
        max_length=100,
        verbose_name='Bairro'
    )
    endereco_cidade = models.CharField(
        max_length=100,
        verbose_name='Cidade'
    )
    endereco_estado = models.CharField(
        max_length=2,
        verbose_name='Estado'
    )
    
    # Status e Valores
    status = models.CharField(
        max_length=20,
        choices=StatusPedido.choices,
        default=StatusPedido.PENDENTE,
        db_index=True,
        verbose_name='Status'
    )
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Subtotal'
    )
    desconto = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Desconto'
    )
    frete = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Frete'
    )
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Total'
    )
    
    # Observações
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )
    observacoes_internas = models.TextField(
        blank=True,
        verbose_name='Observações Internas'
    )
    
    # Datas importantes
    data_entrega_prevista = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Data de Entrega Prevista'
    )
    data_entrega_realizada = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Data de Entrega Realizada'
    )
    
    objects = models.Manager()
    active_objects = ActiveSoftDeleteManager()
    
    class Meta:
        db_table = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['vendedor', 'status']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['numero']),
        ]
    
    def __str__(self):
        return f"Pedido {self.numero} - {self.cliente_nome}"
    
    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = self.gerar_numero()
        if not self.total:
            self.calcular_total()
        super().save(*args, **kwargs)
    
    def gerar_numero(self):
        """Gera número único para o pedido"""
        from datetime import datetime
        import random
        
        # Formato: YYYYMMDD-XXXX
        data = datetime.now().strftime('%Y%m%d')
        numero_sequencial = random.randint(1000, 9999)
        return f"{data}-{numero_sequencial}"
    
    def calcular_total(self):
        """Calcula total do pedido"""
        self.total = self.subtotal + self.frete - self.desconto
        return self.total


class ItemPedido(TimeStampedModel):
    """Itens do pedido"""
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Pedido'
    )
    produto = models.ForeignKey(
        'produtos.Produto',
        on_delete=models.PROTECT,
        verbose_name='Produto'
    )
    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade'
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Preço Unitário'
    )
    preco_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Preço Total'
    )
    
    # Variações do produto
    variacao = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Variação'
    )
    
    class Meta:
        db_table = 'itens_pedido'
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens dos Pedidos'
        unique_together = ['pedido', 'produto', 'variacao']
    
    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}x"
    
    def save(self, *args, **kwargs):
        if not self.preco_total:
            self.preco_total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)


class StatusHistorico(TimeStampedModel):
    """Histórico de mudanças de status do pedido"""
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='historico_status',
        verbose_name='Pedido'
    )
    status_anterior = models.CharField(
        max_length=20,
        choices=StatusPedido.choices,
        verbose_name='Status Anterior'
    )
    status_novo = models.CharField(
        max_length=20,
        choices=StatusPedido.choices,
        verbose_name='Status Novo'
    )
    usuario = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário'
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name='Observações'
    )
    
    class Meta:
        db_table = 'status_historico'
        verbose_name = 'Histórico de Status'
        verbose_name_plural = 'Históricos de Status'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.pedido.numero}: {self.status_anterior} → {self.status_novo}"
