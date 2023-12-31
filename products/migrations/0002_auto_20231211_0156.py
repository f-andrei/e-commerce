# Generated by Django 3.1.6 on 2023-12-11 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_description', models.TextField(max_length=255)),
                ('long_description', models.TextField()),
                ('image', models.ImageField(upload_to='product_images/%Y%m/')),
                ('slug', models.SlugField(unique=True)),
                ('marketing_price', models.FloatField()),
                ('marketing_promotional_price', models.FloatField(default=0)),
                ('type', models.CharField(choices=[('V', 'Variation'), ('S', 'Simple')], default='V', max_length=1)),
            ],
        ),
        migrations.DeleteModel(
            name='Produto',
        ),
    ]
