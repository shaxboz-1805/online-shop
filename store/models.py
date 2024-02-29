from django.db import models
from users.models import User
from django.conf import settings
# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 500)
    price = models.IntegerField()
    is_new = models.BooleanField()
    is_discounted = models.BooleanField(default = False)
    category = models.ForeignKey("Category", null = True,blank=True, on_delete = models.CASCADE)
    brand = models.ForeignKey("Brand", null = True,blank=True, on_delete = models.CASCADE)
    image = models.ImageField()

    def __str__(self) :
        return self.title
    
    def sale_product_price(self):
        if self.is_discounted:
            return self.price * 0.8

class Category(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title
    
    def total_prouct_price(self):
        return self.product.price * self.quantity
    

class Order(models.Model):
    address = models.CharField(max_length = 255)
    phone = models.CharField(max_length = 255)
    total_price = models.IntegerField()
    customer = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return 'Order # %s' % (str(self.id))
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name = 'order_products')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    amount = models.IntegerField()
    total = models.IntegerField()