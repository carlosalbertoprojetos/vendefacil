# Prompt Completo para Desenvolvimento do Sistema VendaSimples

## 📋 Contexto e Objetivo

Desenvolva um sistema completo de catálogo/vitrine de produtos chamado **VendaSimples**, utilizando Django 5.0+. O sistema deve ser robusto, escalável e seguir as melhores práticas de desenvolvimento, permitindo que empresas e vendedores gerenciem produtos e recebam pedidos online através de catálogos personalizados.

---

## 🎯 Características Principais do Sistema

### Visão Geral
- **Nome do Sistema**: VendaSimples
- **Framework**: Django 5.0+
- **Banco de Dados**: PostgreSQL 14+
- **Cache**: Redis 7+
- **Frontend**: Bootstrap 5.3, JavaScript ES6+, jQuery
- **API**: Django REST Framework 3.14+
- **Task Queue**: Celery 5.3+
- **Storage**: AWS S3 (configurável para local)

### Funcionalidades Core
1. Sistema hierárquico de usuários (Superusuário, Empresa, Vendedor)
2. Gestão completa de produtos com upload de múltiplas imagens
3. Catálogos públicos personalizados por vendedor/empresa
4. Carrinho de compras (sessão e persistido)
5. Sistema de pedidos com máquina de estados
6. Múltiplos métodos de pagamento
7. Integração com WhatsApp para pedidos
8. Dashboards personalizados por tipo de usuário
9. Sistema de notificações multi-canal
10. API REST completa com versionamento

---

## 🏗️ Arquitetura e Estrutura

### Arquitetura em Camadas

```
Presentation Layer (Views, Templates, Serializers)
    ↓
Service Layer (Business Logic, Workflows)
    ↓
Repository Layer (Data Access, Query Optimization)
    ↓
Data Layer (Models, Database)
```

### Estrutura de Diretórios

```
vendasimples/
├── config/                           # Configurações
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                             # Aplicações Django
│   ├── core/                         # Shared utilities
│   │   ├── models.py                 # TimeStampedModel, SoftDeleteModel, AuditModel
│   │   ├── managers.py               # ActiveManager, SoftDeleteManager
│   │   ├── mixins.py                 # View mixins reutilizáveis
│   │   ├── validators.py             # CPF, CNPJ, telefone
│   │   ├── exceptions.py
│   │   ├── utils.py
│   │   ├── constants.py
│   │   ├── pagination.py
│   │   ├── templatetags/
│   │   └── middleware/
│   │
│   ├── authentication/               # Sistema de Usuários
│   │   ├── models.py                 # User, Profile, Empresa
│   │   ├── managers.py               # UserManager customizado
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   └── empresa_service.py
│   │   ├── repositories/
│   │   ├── forms.py                  # Login, Register, Profile
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── permissions.py            # Permissões granulares
│   │   ├── decorators.py             # @role_required
│   │   ├── backends.py               # Email authentication
│   │   ├── signals.py
│   │   ├── serializers.py
│   │   ├── context_processors.py
│   │   └── tests/
│   │
│   ├── produtos/                     # Gestão de Produtos
│   │   ├── models.py                 # Produto, Categoria, ImagemProduto
│   │   ├── services/
│   │   │   ├── produto_service.py
│   │   │   ├── categoria_service.py
│   │   │   ├── imagem_service.py
│   │   │   └── estatistica_service.py
│   │   ├── repositories/
│   │   ├── validators/
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── filters.py
│   │   ├── signals.py
│   │   ├── tasks.py                  # Processamento de imagens
│   │   └── tests/
│   │
│   ├── pedidos/                      # Sistema de Pedidos
│   │   ├── models.py                 # Pedido, ItemPedido, StatusHistorico
│   │   ├── services/
│   │   │   ├── pedido_service.py
│   │   │   ├── status_service.py
│   │   │   ├── calculo_service.py
│   │   │   └── notificacao_service.py
│   │   ├── workflows/
│   │   │   └── pedido_state_machine.py
│   │   ├── repositories/
│   │   ├── constants.py              # Status de pedidos
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── signals.py
│   │   ├── tasks.py
│   │   └── tests/
│   │
│   ├── carrinho/                     # Carrinho de Compras
│   │   ├── cart.py                   # Classe Cart principal
│   │   ├── models.py                 # CarrinhoItem (persistido)
│   │   ├── services/
│   │   │   ├── carrinho_sessao_service.py
│   │   │   ├── carrinho_usuario_service.py
│   │   │   └── carrinho_multi_service.py
│   │   ├── forms.py
│   │   ├── views.py                  # APIs AJAX
│   │   ├── urls.py
│   │   ├── context_processors.py
│   │   └── tests/
│   │
│   ├── pagamento/                    # Sistema de Pagamentos
│   │   ├── models.py                 # Pagamento, HistoricoPagamento
│   │   ├── gateways/
│   │   │   ├── base.py               # Interface abstrata
│   │   │   ├── mercadopago.py
│   │   │   ├── pagseguro.py
│   │   │   ├── stripe.py
│   │   │   └── pix.py
│   │   ├── services/
│   │   │   ├── pagamento_service.py
│   │   │   ├── gateway_factory.py
│   │   │   └── troco_service.py
│   │   ├── repositories/
│   │   ├── constants.py              # Métodos e status
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── webhooks.py
│   │   ├── signals.py
│   │   ├── tasks.py
│   │   └── tests/
│   │
│   ├── catalogo/                     # Catálogo Público
│   │   ├── services/
│   │   │   ├── catalogo_service.py
│   │   │   └── compartilhamento_service.py
│   │   ├── views.py                  # Catálogo vendedor/empresa
│   │   ├── urls.py
│   │   ├── filters.py
│   │   ├── context_processors.py
│   │   ├── templatetags/
│   │   └── tests/
│   │
│   ├── configuracoes/                # Configurações
│   │   ├── models.py                 # SiteConfig, ConfigEmpresa, Banner
│   │   ├── services/
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── context_processors.py
│   │   └── tests/
│   │
│   ├── dashboard/                    # Dashboards
│   │   ├── services/
│   │   │   ├── analytics_service.py
│   │   │   ├── report_service.py
│   │   │   └── kpi_service.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   │
│   ├── notificacoes/                 # Notificações
│   │   ├── models.py
│   │   ├── channels/
│   │   │   ├── base.py
│   │   │   ├── email.py
│   │   │   ├── sms.py
│   │   │   ├── whatsapp.py
│   │   │   └── push.py
│   │   ├── services/
│   │   ├── admin.py
│   │   ├── tasks.py
│   │   ├── signals.py
│   │   └── tests/
│   │
│   ├── whatsapp/                     # Integração WhatsApp
│   │   ├── services/
│   │   │   ├── whatsapp_service.py
│   │   │   └── message_builder.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── tests/
│   │
│   ├── estatisticas/                 # Estatísticas
│   │   ├── models.py                 # Visualizacao, Compartilhamento
│   │   ├── services/
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   │
│   └── api/                          # API REST
│       ├── v1/
│       │   ├── urls.py
│       │   ├── views/
│       │   ├── serializers/
│       │   ├── permissions.py
│       │   ├── throttling.py
│       │   └── pagination.py
│       └── docs/
│
├── infrastructure/                   # Infraestrutura
│   ├── storage/
│   ├── cache/
│   ├── logging/
│   ├── monitoring/
│   └── email/
│
├── templates/                        # Templates Django
│   ├── base/
│   │   ├── base.html
│   │   ├── base_auth.html
│   │   ├── base_dashboard.html
│   │   ├── base_catalogo.html
│   │   ├── navbar.html
│   │   ├── sidebar.html
│   │   └── footer.html
│   ├── components/
│   ├── authentication/
│   ├── dashboard/
│   ├── produtos/
│   ├── pedidos/
│   ├── carrinho/
│   ├── catalogo/
│   ├── configuracoes/
│   ├── home/
│   ├── errors/
│   └── emails/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── img/
│   ├── fonts/
│   └── vendor/
│
├── media/
├── locale/
├── docs/
├── scripts/
├── tests/
└── docker/
```

---

## 📊 Modelos de Dados Detalhados

### 1. Core Models (Abstract Base Classes)

```python
# apps/core/models.py

class TimeStampedModel(models.Model):
    """Model abstrato para timestamps automáticos"""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']

class SoftDeleteModel(models.Model):
    """Model abstrato para soft delete"""
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()  # Apenas is_active=True
    
    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False):
        """Soft delete - marca como inativo"""
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()
    
    def hard_delete(self):
        """Delete permanente do banco"""
        super().delete()

class AuditModel(TimeStampedModel):
    """Model abstrato para auditoria de ações"""
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_created',
        verbose_name='Criado por'
    )
    updated_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_updated',
        verbose_name='Atualizado por'
    )
    
    class Meta:
        abstract = True
```

### 2. Authentication Models

```python
# apps/authentication/models.py

class UserRole(models.TextChoices):
    SUPERUSER = 'SUPER', 'Superusuário'
    EMPRESA = 'EMPRESA', 'Empresa'
    VENDEDOR = 'VENDEDOR', 'Vendedor'

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, SoftDeleteModel):
    """Modelo customizado de usuário"""
    email = models.EmailField(unique=True, db_index=True, verbose_name='E-mail')
    first_name = models.CharField(max_length=150, verbose_name='Nome')
    last_name = models.CharField(max_length=150, verbose_name='Sobrenome')
    role = models.CharField(max_length=20, choices=UserRole.choices, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        indexes = [
            models.Index(fields=['email', 'role']),
            models.Index(fields=['is_active', 'role']),
            models.Index(fields=['is_verified', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name
    
    def has_permission(self, permission):
        """Verifica se tem permissão específica"""
        from .permissions import ROLE_PERMISSIONS
        role_permissions = ROLE_PERMISSIONS.get(self.role, [])
        return permission in role_permissions
    
    def can_manage_produto(self, produto):
        """Verifica se pode gerenciar produto"""
        if self.role == UserRole.SUPERUSER:
            return True
        if self.role == UserRole.EMPRESA:
            return produto.vendedor.profile.empresa.user == self
        if self.role == UserRole.VENDEDOR:
            return produto.vendedor == self
        return False
    
    def can_view_pedido(self, pedido):
        """Verifica se pode visualizar pedido"""
        if self.role == UserRole.SUPERUSER:
            return True
        if self.role == UserRole.VENDEDOR:
            return pedido.vendedor == self
        if self.role == UserRole.EMPRESA:
            return pedido.vendedor.profile.empresa.user == self
        return False

class Empresa(TimeStampedModel, SoftDeleteModel):
    """Modelo de empresa"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empresa')
    razao_social = models.CharField(max_length=255, verbose_name='Razão Social')
    nome_fantasia = models.CharField(max_length=255, verbose_name='Nome Fantasia')
    cnpj = models.CharField(max_length=18, unique=True, db_index=True)
    telefone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True)
    endereco = models.CharField(max_length=255, verbose_name='Endereço')
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    
    # Mídia
    logo = models.ImageField(upload_to='empresas/logos/', null=True, blank=True)
    banner = models.ImageField(upload_to='empresas/banners/', null=True, blank=True)
    
    # Configurações
    tema_cor_primaria = models.CharField(max_length=7, default='#2563eb')
    tema_cor_secundaria = models.CharField(max_length=7, default='#64748b')
    
    class Meta:
        db_table = 'empresas'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        indexes = [
            models.Index(fields=['cnpj']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.nome_fantasia
    
    @property
    def total_vendedores(self):
        return self.vendedores.filter(user__is_active=True).count()
    
    @property
    def total_produtos(self):
        from apps.produtos.models import Produto
        return Produto.active_objects.filter(
            vendedor__profile__empresa=self
        ).count()

class Profile(TimeStampedModel):
    """Perfil estendido do usuário"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True, db_index=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    whatsapp = models.CharField(max_length=20, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Relacionamento
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vendedores'
    )
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"
```

### 3. Produtos Models

```python
# apps/produtos/models.py

class Categoria(TimeStampedModel, SoftDeleteModel, AuditModel):
    """Categoria de produtos"""
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='categorias/', null=True, blank=True)
    ordem = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategorias'
    )
    
    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['ordem', 'nome']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'ordem']),
        ]
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

class Produto(TimeStampedModel, SoftDeleteModel, AuditModel):
    """Modelo de produto"""
    # Informações Básicas
    nome = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    descricao = models.TextField()
    descricao_curta = models.CharField(max_length=255, blank=True)
    
    # Preço e Estoque
    preco = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    preco_promocional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    estoque = models.IntegerField(default=0, db_index=True)
    estoque_minimo = models.IntegerField(default=0)
    
    # Identificação
    codigo = models.CharField(max_length=50, unique=True, db_index=True)
    sku = models.CharField(max_length=50, blank=True)
    ean = models.CharField(max_length=13, blank=True)
    marca = models.CharField(max_length=100, blank=True)
    
    # Relacionamentos
    vendedor = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        related_name='produtos'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='produtos'
    )
    
    # Status
    disponivel = models.BooleanField(default=True, db_index=True)
    em_destaque = models.BooleanField(default=False, db_index=True)
    em_promocao = models.BooleanField(default=False, db_index=True)
    mais_vendido = models.BooleanField(default=False, db_index=True)
    lancamento = models.BooleanField(default=False, db_index=True)
    
    # Dimensões e Peso
    peso = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    largura = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    comprimento = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Estatísticas
    visualizacoes = models.IntegerField(default=0)
    vendas = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'produtos'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['vendedor', 'is_active']),
            models.Index(fields=['categoria', 'is_active']),
            models.Index(fields=['preco']),
            models.Index(fields=['estoque']),
            models.Index(fields=['codigo']),
            models.Index(fields=['em_destaque', 'is_active']),
            models.Index(fields=['disponivel', 'is_active']),
        ]
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        if not self.codigo:
            self.codigo = self.gerar_codigo()
        super().save(*args, **kwargs)
    
    def gerar_codigo(self):
        """Gera código único para o produto"""
        import random
        import string
        while True:
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not Produto.objects.filter(codigo=codigo).exists():
                return codigo
    
    @property
    def preco_final(self):
        """Retorna preço promocional se disponível, senão preço normal"""
        if self.em_promocao and self.preco_promocional:
            return self.preco_promocional
        return self.preco
    
    @property
    def tem_estoque(self):
        return self.estoque > 0
    
    @property
    def estoque_baixo(self):
        return self.estoque <= self.estoque_minimo
    
    @property
    def imagem_principal(self):
        """Retorna primeira imagem ou None"""
        return self.imagens.filter(is_principal=True).first() or self.imagens.first()

class ImagemProduto(TimeStampedModel):
    """Imagens do produto"""
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='produtos/imagens/')
    thumbnail = models.ImageField(upload_to='produtos/thumbnails/', null=True, blank=True)
    is_principal = models.BooleanField(default=False)
    ordem = models.IntegerField(default=0)
    alt_text = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'imagens_produto'
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens dos Produtos'
        ordering = ['ordem', 'created_at']
    
    def __str__(self):
        return f"Imagem de {self.produto.nome}"
    
    def save(self, *args, **kwargs):
        # Se marcada como principal, desmarca outras
        if self.is_principal:
            ImagemProduto.objects.filter(
                produto=self.produto,
                is_principal=True
            ).exclude(pk=self.pk).update(is_principal=False)
        super().save(*args, **kwargs)
```

### 4. Pedidos Models

```python
# apps/pedidos/models.py

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
    numero = models.CharField(max_length=20, unique=True, db_index=True)
    
    # Relacionamentos
    vendedor = models.ForeignKey(
        'authentication.User',
        on_delete=models.PROTECT,
        related_name='pedidos_vendedor'
    )
    cliente_usuario = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos_cliente'
    )
    
    # Dados do Cliente
    cliente_nome = models.CharField(max_length=255)
    cliente_telefone = models.CharField(max_length=20)
    cliente_email = models.EmailField(blank=True)
    cliente_cpf = models.CharField(max_length=14, blank=True)
    
    # Endereço de Entrega
    endereco_cep = models.CharField(max_length=9)
    endereco_logradouro = models.CharField(max_length=255)
    endereco_numero = models.CharField(max_length=20)
    endereco_complemento = models.CharField(max_length=100, blank=True)
    endereco_bairro = models.CharField(max_length=100)
    endereco_cidade = models.CharField(max_length=100)
    endereco_estado = models.CharField(max_length=2)
    
    # Status e Valores
    status = models.CharField(
        max_length=20,
        choices=StatusPedido.choices,
        default=StatusPedido.PENDENTE,
        db_index=True
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frete = models.DecimalField(max_digits=10, decimal_places=2