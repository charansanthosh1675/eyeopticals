from django.contrib import admin
from .models import Product, Customer, Order, Cart, CartItem

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)