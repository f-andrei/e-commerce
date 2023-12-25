from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_price(val):
    return utils.format_price(val)

@register.filter
def cart_count(cart):
    return utils.cart_count(cart)

@register.filter
def cart_total(cart):
    return utils.cart_total(cart)

@register.filter
def format_long_description(description):
    return utils.format_long_description(description)