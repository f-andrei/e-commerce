from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class InlineOrderItem(admin.TabularInline):
    model = OrderItem
    extra = 1


class AdminOrder(admin.ModelAdmin):
    inlines = [
        InlineOrderItem
    ]


admin.site.register(Order, AdminOrder)
admin.site.register(OrderItem)