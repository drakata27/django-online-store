from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from . models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from . utils import *
import stripe
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()
stripe.api_key=settings.STRIPE_SECRET_KEY
endpoint_secret=settings.STRIPE_WEBHOOK_KEY

def home(request):
    featured_products = Product.objects.filter(image__istartswith='f')
    new_products = Product.objects.filter(image__istartswith='n')

    guest_data = cart_data(request)
    cart_items = guest_data['cart_items']

    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'cart_items' : cart_items,
    }
    return render(request, 'store/home.html', context)


def cart(request):
    guest_data = cart_data(request)
    cart_items = guest_data['cart_items']
    order = guest_data['order']
    items = guest_data['items']
            
    context = {
        'items':items,
        'order': order, 
        'cart_items': cart_items,
        }
    return render(request, 'store/cart.html', context )

def checkout(request):
    guest_data = cart_data(request)
    cart_items = guest_data['cart_items']
    order = guest_data['order']
    items = guest_data['items']

    context = {
        'items': items, 
        'order': order,
        'get_cart_items': 0,
        'cart_items': cart_items,
    }   
    return render(request, 'store/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(productId)
    print(action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()       

    return JsonResponse('Item was updated', safe=False)

def shop(request):
    featured_products = Product.objects.filter(image__istartswith='f')
    new_products = Product.objects.filter(image__istartswith='n')

    guest_data = cart_data(request)
    cart_items = guest_data['cart_items']
    items = guest_data['items']

    context = {
        'items': items,
        'featured_products': featured_products,
        'new_products': new_products,
        'cart_items' : cart_items,
    }
    return render(request, 'store/shop.html', context)

def blog(request):
    guest_data = cart_data(request)
    cart_items = guest_data['cart_items']
        
    context = {
        'cart_items': cart_items,
        }
    return render(request, 'store/blog.html', context)

def about(request):
    guest_data = cart_data(request)
    cart_items = guest_data['cart_items']
        
    context = {
        'cart_items': cart_items,
        }
    return render(request, 'store/about.html', context)

def contact(request):
    guest_data = cart_data(request)
    cart_items = guest_data['cart_items']
        
    context = {
        'cart_items': cart_items,
        }
    return render(request, 'store/contact.html', context)

def checkout_session(request):
    DOMAIN = 'http://' + os.getenv('HOST_AND_PORT') + '/'
    line_items = []

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
        items = order.orderitem_set.all()
        
        for item in items:
            product = item.product
            quantity = item.quantity
            line_item = {
                'price': product.price_id,
                'quantity': quantity,
            }
            line_items.append(line_item)
    else:
        guest_data = cart_data(request)
        items = guest_data['items']
    
        for item in items:
            product = item['product']
            quantity = item['quantity']
            line_item = {
                'price': product['price_id'],
                'quantity': quantity,
            }
            line_items.append(line_item)

    checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=DOMAIN,
            cancel_url=DOMAIN + '/checkout',
        ) 
    
    return redirect(checkout_session.url, code=303)

@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', None)
    event = None

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
        event['data']['object']['id'],
        expand=['line_items'],
        )

        total = float(data['data']['object']['amount_total'])/100
        customer, order = guest_order(request, data)
        order.transaction_id = transaction_id

        print('Total', total)
        print('Order.get_cart_total', order.get_cart_total)
        print('Order', order)

        order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['data']['object']['customer_details']['address']['line1'],
            city=data['data']['object']['customer_details']['address']['city'],
            postcode=data['data']['object']['customer_details']['address']['postal_code'],
        )

        print(session)
        print('Data:',data)
        print("Order completed!")
            

    return HttpResponse(status=200)
