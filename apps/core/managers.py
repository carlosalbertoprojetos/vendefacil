"""
Custom managers for VendaSimples project.
"""

from django.db import models


class ActiveManager(models.Manager):
    """Manager que retorna apenas objetos ativos"""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class SoftDeleteManager(models.Manager):
    """Manager que retorna apenas objetos não deletados"""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class ActiveSoftDeleteManager(models.Manager):
    """Manager que retorna apenas objetos ativos e não deletados"""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, deleted_at__isnull=True)
