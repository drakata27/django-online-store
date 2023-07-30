from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('shop/', views.shop, name='shop'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('update_item/', views.update_item, name='update_item'),
    # stripe 
    path('checkout_session/', views.checkout_session, name='checkout_session'),
    path('webhook/', views.webhook, name='webhook'),
]