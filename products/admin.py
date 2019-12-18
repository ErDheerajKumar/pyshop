from django.contrib import admin
from .models import Product, OrderInCart, Order, Coupon, Returns, Address


def make_return_accepted(modeladmin, request, queryset):
    queryset.update(return_request=False, return_result=True)


make_return_accepted.short_description = "Update order to return successful"


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'image']
    list_filter = ['stock', 'price']
    search_fields = ['name', 'stock']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'Out_for_delivery',
                    'delivered',
                    'return_request',
                    'return_result',
                    'billing_address',
                    'shipping_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = ['user',
                          'billing_address',
                          'shipping_address',
                          'payment',
                          'coupon'
                          ]
    list_filter = ['ordered',
                   'Out_for_delivery',
                   'delivered',
                   'return_request',
                   'return_result'
                   ]
    search_fields = ['user__username',
                     'order_id'
                     ]
    actions = [
                make_return_accepted
               ]


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'amount')


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'address_line_1',
                    'address_line_2',
                    'country',
                    'state',
                    'city',
                    'pin_code',
                    'address_type',
                    'default'
                    ]
    list_filter = [
                   'address_type',
                   'default',
                   'country',
                   ]
    search_fields = ['user',
                     'state',
                     'city',
                     'pin_code',

                     ]


admin.site.register(Product, ProductAdmin)
admin.site.register(OrderInCart)
admin.site.register(Order, OrderAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Address, AddressAdmin)
