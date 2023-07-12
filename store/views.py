from django.shortcuts import render
from . models import Product, Customer, OrderItem, Order

def home(request):
    featured_products = Product.objects.filter(image__istartswith='f')
    new_products = Product.objects.filter(image__istartswith='n')
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
    }
    return render(request, 'store/home.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)        
        items = order.orderitem_set.all()
        print('User is authenticated')
    else:
        print('User is not authenticated')
        items=[]

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context )

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)