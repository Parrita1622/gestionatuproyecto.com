# Generated by Django 4.1.1 on 2023-10-29 22:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cabin_APP', '0038_userprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='UsuarioExtendido',
        ),
        migrations.RenameField(
            model_name='usuarioextendido',
            old_name='user',
            new_name='usuario',
        ),
    ]
