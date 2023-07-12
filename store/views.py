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

def shop(request):
    context = {}
    return render(request, 'store/shop.html', context)

def blog(request):
    context = {}
    return render(request, 'store/blog.html', context)

def about(request):
    context = {}
    return render(request, 'store/about.html', context)

def contact(request):
    context = {}
    return render(request, 'store/contact.html', context)