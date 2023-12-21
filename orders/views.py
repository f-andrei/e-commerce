from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from products.models import Variation
from utils import utils
from .models import Order, OrderItem

# Create your views here.
class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('users:create')

        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs

class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'



class CloseOrder(View):
    template_name = 'order/pay.html'
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Faça login para acessar esta página.'
            )
            return redirect('users:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('products:list')

        cart = self.request.session.get('cart')
        cart_vartiation_ids = [v for v in cart]
        
        db_variations = list(Variation.objects.select_related('product') \
                            .filter(id__in=cart_vartiation_ids))
        for variation in db_variations:
            variation_id = str(variation.id)
            inventory = variation.inventory
            cart_quantity = cart[variation_id]['quantity']
            unity_price = cart[variation_id]['unit_price']
            promotional_unity_price = cart[variation_id]['promotional_unit_price']

            error_msg = ''

            if inventory == 0:
                error_msg = 'Um ou mais produtos foram esgotados. ' \
                'Atualizamos o seu carrinho.'
                del cart[variation_id]

            elif inventory < cart_quantity:
                cart[variation_id]['quantity'] = inventory
                cart[variation_id]['quantity_price'] = inventory * unity_price
                cart[variation_id]['promotional_quantity_price'] = inventory * \
                    promotional_unity_price
                
                error_msg = 'Estoque insuficiente para um ou mais produtos do seu ' \
                'carrinho. Verifique novamente seu pedido com a quantidade ' \
                'reduzida. O preço total também foi atualizado.'


            if error_msg:
                messages.warning(
                    self.request,
                    error_msg
                )

                self.request.session.save()
                return redirect('products:cart')
            
        cart_total_quantity = utils.cart_count(cart)
        cart_total_value = utils.cart_total(cart)

        order = Order(
            user=self.request.user,
            total=cart_total_value,
            total_quantity=cart_total_quantity,
            status='C'
        )
        
        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantity_price'],
                    promotional_price=v['promotional_quantity_price'],
                    quantity=v['quantity'],
                    image=v['image']
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']

        return redirect(
            reverse(
                'orders:pay',
                kwargs={
                    'pk': order.pk
                }
            )
        )


class Detail(DispatchLoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order/detail.html'
    pk_url_kwarg = 'pk'


class ViewOrder(DispatchLoginRequiredMixin, ListView): 
    model = Order
    context_object_name = 'orders'
    template_name = 'order/view_order.html'
    paginate_by = 10
    ordering = ['-id']

    


