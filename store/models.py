from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    # def __str__(self) -> str:
    #     return self.user
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    brand = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)
    price_id = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name + ' ' + str(self.id)


    # if there is no image the page won't crash but render the page without the image
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# The whole cart
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return str(self.id)
    
    # Total value of cart
    @property
    def get_cart_total(self):
        #retrieves all the related OrderItem objects via reverse relation
        orderitems=self.orderitem_set.all()

        total = sum([item.get_total for item in orderitems]) 
        return total
    
    # Calculates how many items are in the cart e.g 2 Watches + 1 Book = 3 items
    @property
    def get_cart_items(self):
        #retrieves all the related OrderItem objects via reverse relation
        orderitems=self.orderitem_set.all()

        total = sum([item.quantity for item in orderitems])
        return total

# A single item in the cart
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)
    
    # total price for a single product in terms of its qty
    @property
    def get_total(self):
        return self.product.price * self.quantity

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address





