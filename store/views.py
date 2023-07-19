from django.shortcuts import render, redirect
from django.http import JsonResponse
from . models import *
import datetime
import json
from . utils import *
import stripe
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()

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
        'items': items, 'order': order,
        'get_cart_items': 0,
        'cart_items': cart_items,
        'checkout_session_url' : None,
    }
    
    if request.method == 'POST':
        # Call the checkout_session function to initiate the Stripe checkout
        checkout_session_url = checkout_session()
        context['checkout_session_url'] = checkout_session_url
    
        
    return render(request, 'store/checkout.html', context)

def updateItem(request):
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


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id 

    if total == float(order.get_cart_total):
        order.complete=True
        print('Added to the DB')
    else:
        print('Not the same values')
    order.save()

    print('Data type of total:', type(total))
    print('Data type of get_total:', type(order.get_cart_total))

    ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            postcode = data['shipping']['postcode'],
    )

     # TEST STRIPE
 
    return JsonResponse('Payment submitted...', safe=False)

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

def checkout_session():
    # TEST STRIPE
    DOMAIN = 'http://' + os.getenv('HOST_AND_PORT') + '/'
    stripe.api_key=settings.STRIPE_SECRET_KEY
    
    checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 'price_1NVZHxKEjjyTT4MxUrxfXRHU',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=DOMAIN,
            cancel_url=DOMAIN,
        )
    
    return redirect(checkout_session.url, code=303)
