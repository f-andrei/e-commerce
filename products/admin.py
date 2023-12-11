from django.contrib import admin
from .models import Product, Variation

# Register your models here.

class InlineVariation(admin.TabularInline):
    model = Variation
    extra = 1

class AdminProduct(admin.ModelAdmin):
    inlines = [
        InlineVariation
    ]

admin.site.register(Product, AdminProduct)
admin.site.register(Variation)