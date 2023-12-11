from django.contrib import admin
from .models import Product, Variation

# Register your models here.

class InlineVariation(admin.TabularInline):
    model = Variation
    extra = 1

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'short_description', 'get_formatted_price', 'get_formatted_promotional_price']
    inlines = [
        InlineVariation
    ]

admin.site.register(Product, AdminProduct)
admin.site.register(Variation)