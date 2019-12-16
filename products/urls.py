from django.urls import path
from . import views
from .views import (
    ItemDetailView,
    HomeView,
    CheckoutView,
    add_to_cart,
    remove_from_cart,
    OrderSummeryView,
    remove_single_product_from_cart,
    add_single_product_to_cart,
    PaymentView,
    AddCouponView

)

app_name = 'products'
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('products', views.Product, name='products'),
    path('products/<slug>/', ItemDetailView.as_view(), name='products'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('add_coupon/', AddCouponView.as_view(), name='add_coupon'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('order_summery', OrderSummeryView.as_view(), name='order_summery'),
    path('remove_single_product_from_cart/<slug>/', remove_single_product_from_cart, name='remove_single_product_from_cart'),
    path('add_single_product_to_cart/<slug>/', add_single_product_to_cart, name='add_single_product_to_cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment')

]
