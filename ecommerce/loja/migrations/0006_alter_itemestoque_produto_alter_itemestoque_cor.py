# Generated by Django 5.1 on 2024-09-04 23:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0005_cor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemestoque',
            name='Produto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.produto'),
        ),
        migrations.AlterField(
            model_name='itemestoque',
            name='cor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loja.cor'),
        ),
    ]