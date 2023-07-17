from . models import *
import json

def guest_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:',cart)
    items=[]
    order = {'get_cart_total':0, 'get_cart_items':0,}
    cart_items = order['get_cart_items']

    for i in cart:
        try:
            cart_items += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
        except:
            pass

    guest_data = {
        'items': items, 
        'order': order, 
        'cart_items': cart_items,
    }
    
    return guest_data