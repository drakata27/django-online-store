from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('update-item/', views.update_item, name='update_item'),
    path('thank-you/', views.thank_you, name='thank_you'),
    # stripe 
    path('checkout_session/', views.checkout_session, name='checkout_session'),
    path('webhook/', views.webhook, name='webhook'),
]