"""
Admin configuration for authentication app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Empresa


class ProfileInline(admin.StackedInline):
    """Inline para perfil do usuário"""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'


class UserAdmin(BaseUserAdmin):
    """Admin customizado para User"""
    inlines = (ProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_verified', 'created_at')
    list_filter = ('role', 'is_active', 'is_verified', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'role', 'phone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


class EmpresaAdmin(admin.ModelAdmin):
    """Admin para Empresa"""
    list_display = ('nome_fantasia', 'razao_social', 'cnpj', 'cidade', 'estado', 'is_active')
    list_filter = ('is_active', 'estado', 'created_at')
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'razao_social', 'nome_fantasia', 'cnpj')
        }),
        ('Contato', {
            'fields': ('telefone', 'whatsapp', 'email')
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Mídia', {
            'fields': ('logo', 'banner')
        }),
        ('Personalização', {
            'fields': ('tema_cor_primaria', 'tema_cor_secundaria')
        }),
        ('Status', {
            'fields': ('is_active', 'deleted_at')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProfileAdmin(admin.ModelAdmin):
    """Admin para Profile"""
    list_display = ('user', 'cpf', 'telefone', 'cidade', 'empresa')
    list_filter = ('empresa', 'estado', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'cpf')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user', 'empresa')
        }),
        ('Informações Pessoais', {
            'fields': ('cpf', 'telefone', 'whatsapp', 'data_nascimento', 'avatar')
        }),
        ('Endereço', {
            'fields': ('cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Profile, ProfileAdmin)
