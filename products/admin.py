from django.contrib import admin
from .models import Product, OrderInCart, Order, Coupon


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'image')
    list_filter = ('stock', 'price')
    search_fields = ('name', 'stock')


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'amount')


admin.site.register(Product, ProductAdmin)
admin.site.register(OrderInCart)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
