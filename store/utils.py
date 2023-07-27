from . models import *
import json

def guest_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

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
                    'brand': product.brand,
                    'imageURL': product.imageURL,
                    'price_id': product.price_id,
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
    print('Cart:',cart)
    return guest_data

def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        print('Items when the user is logged in', items)
    else:
        guest_data = guest_cart(request)
        cart_items = guest_data['cart_items']
        order = guest_data['order']
        items = guest_data['items']
        print('Items when the user is logged out', items)

    data = {
        'items': items, 
        'order': order, 
        'cart_items': cart_items,
    }
    
    return data

def guest_order(request, data):
    name = data['data']['object']['customer_details']['name']
    email = data['data']['object']['customer_details']['email']

    guest_data = guest_cart(request)
    items = guest_data['items']

    customer, created = Customer.objects.get_or_create(email=email,)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )

    return customer, order