# Generated by Django 5.2.4 on 2025-07-25 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prisoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('numero_documento', models.CharField(max_length=100)),
                ('numero_bo', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('placa', models.CharField(max_length=100)),
                ('delito', models.CharField(max_length=100)),
                ('data', models.DateField()),
                ('estrutura_criminal', models.CharField(max_length=100)),
            ],
        ),
    ]
