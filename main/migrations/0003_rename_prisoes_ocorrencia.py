# Generated by Django 5.2.4 on 2025-07-26 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_prisoes_numero_bo_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Prisoes',
            new_name='Ocorrencia',
        ),
    ]
