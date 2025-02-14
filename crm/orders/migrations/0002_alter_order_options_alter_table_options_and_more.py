# Generated by Django 4.2.18 on 2025-01-31 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'default_related_name': 'orders', 'ordering': ('-created_at',), 'verbose_name': 'заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'ordering': ('number',), 'verbose_name': 'стол заказов', 'verbose_name_plural': 'Столы заказов'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, help_text='Может содержать символы латиницы, цифры, дефис, подчёркивание.', max_length=256, unique=True, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='slug',
            field=models.SlugField(blank=True, help_text='Может содержать символы латиницы, цифры, дефис, подчёркивание.', max_length=256, unique=True, verbose_name='Идентификатор'),
        ),
    ]
