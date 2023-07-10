from django.shortcuts import render
from . models import Product

def home(request):
    featured_products = Product.objects.filter(image__istartswith='f')
    new_products = Product.objects.filter(image__istartswith='n')
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
    }
    return render(request, 'store/home.html', context)


def cart(request):
    context={}
    return render(request, 'store/cart.html', context )

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)