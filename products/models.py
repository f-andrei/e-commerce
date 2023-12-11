from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify
from random import randint
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    short_description = models.TextField(max_length=255, verbose_name='Descrição')
    long_description = models.TextField()
    image = models.ImageField(
        upload_to='product_images/%Y%m/',
        blank=False,
        null=False
        )
    slug = models.SlugField(unique=True, blank=True, null=True)
    marketing_price = models.FloatField(verbose_name='Preço')
    marketing_promotional_price = models.FloatField(default=0, verbose_name='Preço promocional')
    type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variable'),
            ('S', 'Simple'),
        )
    )

    def get_formatted_price(self):
        return f'R$: {self.marketing_price:.2f}'.replace('.', ',')
    
    get_formatted_price.short_description = 'Preço'
    
    def get_formatted_promotional_price(self):
        return f'R$: {self.marketing_promotional_price:.2f}'.replace('.', ',')
    
    get_formatted_promotional_price.short_description = 'Preço Promocional'

    @staticmethod
    def resize_image(img, new_width=800):
        img_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_path)
        width, height = img_pil.size

        if width <= new_width:
            img_pil.close()
            return
        
        new_height = round((new_width * height) / width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_path,
            optimize=True,
            quality=50
        )


    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}-{randint(1, 100) + randint(1, 9)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_size = 800

        if self.image:
            self.resize_image(self.image, max_size)

    def __str__(self):
        return self.name


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    inventory = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name or self.product.name
    
    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'