"""
Core abstract models for VendaSimples project.
"""

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Model abstrato para timestamps automáticos"""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModel(models.Model):
    """Model abstrato para soft delete"""
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Excluído em')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Ativo')
    
    objects = models.Manager()
    
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
        blank=True,
        related_name='%(class)s_created',
        verbose_name='Criado por'
    )
    updated_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name='Atualizado por'
    )
    
    class Meta:
        abstract = True


class ActiveManager(models.Manager):
    """Manager que retorna apenas objetos ativos"""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class SoftDeleteManager(models.Manager):
    """Manager que retorna apenas objetos não deletados"""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
