# Generated by Django 4.1.1 on 2023-09-12 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabin_APP', '0022_delete_admin_remove_papelerareciclaje_maestro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='asociarmaterial',
            name='cantidad_devuelta',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
