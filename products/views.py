from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models

# Create your views here.

class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10



class ProductDetails(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhes do produto')

class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Adicionar ao carrinho')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover do carrinho')


class Cart(ListView):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')


class Finish(ListView):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')

