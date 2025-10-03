"""
Authentication models for VendaSimples project.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, SoftDeleteModel, AuditModel
from apps.core.validators import validate_cpf, validate_cnpj, validate_phone, validate_cep
from .managers import UserManager


class UserRole(models.TextChoices):
    SUPERUSER = 'SUPER', 'Superusuário'
    EMPRESA = 'EMPRESA', 'Empresa'
    VENDEDOR = 'VENDEDOR', 'Vendedor'


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, SoftDeleteModel):
    """Modelo customizado de usuário"""
    email = models.EmailField(
        unique=True, 
        db_index=True, 
        verbose_name='E-mail'
    )
    first_name = models.CharField(
        max_length=150, 
        verbose_name='Nome'
    )
    last_name = models.CharField(
        max_length=150, 
        verbose_name='Sobrenome'
    )
    role = models.CharField(
        max_length=20, 
        choices=UserRole.choices, 
        db_index=True,
        verbose_name='Função'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Acesso ao Admin'
    )
    is_verified = models.BooleanField(
        default=False, 
        db_index=True,
        verbose_name='E-mail Verificado'
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        validators=[validate_phone],
        verbose_name='Telefone'
    )
    
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
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='empresa'
    )
    razao_social = models.CharField(
        max_length=255, 
        verbose_name='Razão Social'
    )
    nome_fantasia = models.CharField(
        max_length=255, 
        verbose_name='Nome Fantasia'
    )
    cnpj = models.CharField(
        max_length=18, 
        unique=True, 
        db_index=True,
        validators=[validate_cnpj],
        verbose_name='CNPJ'
    )
    telefone = models.CharField(
        max_length=20,
        validators=[validate_phone],
        verbose_name='Telefone'
    )
    whatsapp = models.CharField(
        max_length=20, 
        blank=True,
        validators=[validate_phone],
        verbose_name='WhatsApp'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='E-mail'
    )
    
    # Endereço
    cep = models.CharField(
        max_length=9, 
        blank=True,
        validators=[validate_cep],
        verbose_name='CEP'
    )
    endereco = models.CharField(
        max_length=255, 
        verbose_name='Endereço'
    )
    numero = models.CharField(
        max_length=20,
        verbose_name='Número'
    )
    complemento = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='Complemento'
    )
    bairro = models.CharField(
        max_length=100,
        verbose_name='Bairro'
    )
    cidade = models.CharField(
        max_length=100,
        verbose_name='Cidade'
    )
    estado = models.CharField(
        max_length=2,
        verbose_name='Estado'
    )
    
    # Mídia
    logo = models.ImageField(
        upload_to='empresas/logos/', 
        null=True, 
        blank=True,
        verbose_name='Logo'
    )
    banner = models.ImageField(
        upload_to='empresas/banners/', 
        null=True, 
        blank=True,
        verbose_name='Banner'
    )
    
    # Configurações
    tema_cor_primaria = models.CharField(
        max_length=7, 
        default='#2563eb',
        verbose_name='Cor Primária'
    )
    tema_cor_secundaria = models.CharField(
        max_length=7, 
        default='#64748b',
        verbose_name='Cor Secundária'
    )
    
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
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        null=True, 
        blank=True, 
        db_index=True,
        validators=[validate_cpf],
        verbose_name='CPF'
    )
    telefone = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        validators=[validate_phone],
        verbose_name='Telefone'
    )
    whatsapp = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        validators=[validate_phone],
        verbose_name='WhatsApp'
    )
    data_nascimento = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Data de Nascimento'
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        null=True, 
        blank=True,
        verbose_name='Avatar'
    )
    
    # Relacionamento
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vendedores',
        verbose_name='Empresa'
    )
    
    # Endereço
    cep = models.CharField(
        max_length=9, 
        blank=True,
        validators=[validate_cep],
        verbose_name='CEP'
    )
    endereco = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name='Endereço'
    )
    numero = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name='Número'
    )
    complemento = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='Complemento'
    )
    bairro = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='Bairro'
    )
    cidade = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='Cidade'
    )
    estado = models.CharField(
        max_length=2, 
        blank=True,
        verbose_name='Estado'
    )
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"
