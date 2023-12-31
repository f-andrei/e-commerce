# Generated by Django 3.1.6 on 2023-12-12 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20231211_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='marketing_price',
            field=models.FloatField(verbose_name='Preço'),
        ),
        migrations.AlterField(
            model_name='product',
            name='marketing_promotional_price',
            field=models.FloatField(default=0, verbose_name='Preço promocional'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.TextField(max_length=255, verbose_name='Descrição'),
        ),
    ]
