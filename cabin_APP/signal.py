from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import PlanUsuario

@receiver(post_save, sender=User)
def crear_plan_usuario(sender, instance, created, **kwargs):
    if created:
        PlanUsuario.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_plan_usuario(sender, instance, **kwargs):
    instance.planusuario.save()
