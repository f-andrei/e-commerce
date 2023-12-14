def format_price(val):
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_count(cart):
    return sum([item['quantity'] for item in cart.values()])

def cart_total(cart):
    return sum([
        item['promotional_quantity_price']
        if item.get('promotional_quantity_price')
        else item.get('quantity_price')
        for item in cart.values()
    ])