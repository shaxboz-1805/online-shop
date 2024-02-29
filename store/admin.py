from django.contrib import admin
from .models import Product, Category, Brand,Cart,Order,OrderProduct
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderProduct)
