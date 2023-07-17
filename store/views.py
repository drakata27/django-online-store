from django.shortcuts import render
from django.http import JsonResponse
from . models import Product, Customer, OrderItem, Order, ShippingAddress
import datetime
import json

def home(request):
    featured_products = Product.objects.filter(image__istartswith='f')
    new_products = Product.objects.filter(image__istartswith='n')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, }
        cart_items = order['get_cart_items']

    context = {
        'items': items,
        'featured_products': featured_products,
        'new_products': new_products,
        'cart_items' : cart_items,
    }
    return render(request, 'store/home.html', context)


def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
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
            
    context = {
        'items': items, 
        'order': order, 
        'cart_items': cart_items,
        }
    return render(request, 'store/cart.html', context )

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, }
        cart_items = order['get_cart_items']
        
    context = {
        'items': items, 'order': order,
        'get_cart_items': 0,
        'cart_items': cart_items,
        }
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
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete=True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            postcode = data['shipping']['postcode'],
        )
    else:
        print('User is not logged in')
    return JsonResponse('Payment submitted...', safe=False)

def shop(request):
    featured_products = Product.objects.filter(image__istartswith='f')
    new_products = Product.objects.filter(image__istartswith='n')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, }
        cart_items = order['get_cart_items']

    context = {
        'items': items,
        'featured_products': featured_products,
        'new_products': new_products,
        'cart_items' : cart_items,
    }
    return render(request, 'store/shop.html', context)

def blog(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, }
        cart_items = order['get_cart_items']
        
    context = {
        'items': items, 'order': order,
        'get_cart_items': 0,
        'cart_items': cart_items,
        }
    return render(request, 'store/blog.html', context)

def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, }
        cart_items = order['get_cart_items']
        
    context = {
        'items': items, 'order': order,
        'get_cart_items': 0,
        'cart_items': cart_items,
        }
    return render(request, 'store/about.html', context)

def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, }
        cart_items = order['get_cart_items']
        
    context = {
        'items': items, 'order': order,
        'get_cart_items': 0,
        'cart_items': cart_items,
        }
    return render(request, 'store/contact.html', context)
