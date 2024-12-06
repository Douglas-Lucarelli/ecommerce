# Generated by Django 5.1 on 2024-09-03 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0002_alter_produto_imagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='')),
                ('link_destivo', models.CharField(blank=True, max_length=400, null=True)),
                ('ativo', models.BooleanField(default=False)),
            ],
        ),
    ]
