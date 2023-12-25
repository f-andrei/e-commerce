from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from . import models
from users.models import Profile

# Create your views here.

class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']


class ProductDetails(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        if 'search' in self.request.path:
            return self.model.objects.all()
        
        return super().get_queryset()

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        
        if queryset is None:
            queryset = self.get_queryset()
        
        return get_object_or_404(queryset, slug=slug)

class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            resolve_url('products:list')
            )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'Product not found.'
            )
            return redirect(http_referer)
        
        variation = get_object_or_404(models.Variation, id=variation_id)

        variation_inventory = variation.inventory

        product = variation.product
        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        variation_id = variation_id
        unit_price = variation.price
        promotional_unit_price = variation.promotional_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        

        if variation.inventory < 1:
            messages.error(
                self.request,
                'Out of stock.'
            )
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']
        
        if variation_id in cart:
            cart_total_items = cart[variation_id]['quantity']
            cart_total_items += 1

            if variation_inventory < cart_total_items:
                messages.warning(
                    self.request,
                    f"Unfortunately, we only had {variation_inventory} " \
                    "of your chosen item remaining. " \
                    "We've added them all to your cart. " \
                    "Would you like to browse other options?"
                )
                cart_total_items = variation_inventory


            cart[variation_id]['quantity'] = cart_total_items
            cart[variation_id]['quantity_price'] = unit_price * cart_total_items
            cart[variation_id]['promotional_quantity_price'] = \
                promotional_unit_price * cart_total_items
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'promotional_unit_price': promotional_unit_price,
                'quantity_price': unit_price,
                'promotional_quantity_price': promotional_unit_price,
                'quantity': 1,
                'slug': slug,
                'image': image,
                }

        self.request.session.save()

        messages.success(
            self.request,
            f"Product {product_name} {variation_name} successfully added to cart "
            f"{cart[variation_id]['quantity']}x."
            
        )

        return redirect(http_referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            resolve_url('products:list')
            )
        variation_id = self.request.GET.get('vid')
        if not variation_id:
            return redirect(http_referer)
        
        if not self.request.session.get('cart'):
            return redirect(http_referer)
        
        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)
        
        cart = self.request.session['cart'][variation_id]

        messages.success(
            self.request,
            f"Product {cart['product_name']} {cart['variation_name']} " \
            f"removed from your cart."
        )
        
        del self.request.session['cart'][variation_id]
        self.request.session.save()
    
        return redirect(http_referer)


class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {})
        }
        return render(self.request, 'product/cart.html', context)

#TODO: calculate shipping fee
class Overview(ListView):
    def get(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect('users:create')
        
        profile = Profile.objects.filter(user=self.request.user).exists()
        if not profile:
            messages.error(
                self.request,
                'Usuário faltando dados.'
            )
            return redirect('users:create')
        
        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('products:list')

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
        }
        return render(self.request, 'product/overview.html', context)


class Search(ListProducts):
    def get_queryset(self, *args, **kwargs):
        term = self.request.GET.get('term') or self.request.session['term']
        qs = super().get_queryset(*args, **kwargs)

        if not term:
            return qs
        
        self.request.session['term'] = term
        
        qs = qs.filter(
            Q(name__icontains=term) |
            Q(short_description__icontains=term) |
            Q(long_description__icontains=term)
        )

        self.request.session.save()

        return qs
    

class Home(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/home.html')
    

class About(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/about.html')
