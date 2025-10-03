"""
Signals for authentication app.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, Empresa


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria perfil automaticamente quando usuário é criado"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salva perfil quando usuário é salvo"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=Empresa)
def empresa_created(sender, instance, created, **kwargs):
    """Ações quando empresa é criada"""
    if created:
        # Aqui você pode adicionar lógica adicional
        # como enviar email de boas-vindas, etc.
        pass
