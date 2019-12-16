from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderInCart, BillingAddress, Coupon
from django.views.generic import ListView, DetailView, View
from django.views.generic import ListView
from django.utils import timezone
from .forms import CheckoutForm, CouponForm


class HomeView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'index.html'


class ItemDetailView(DetailView):
    model = Product
    template_name = 'products.html'


class OrderSummeryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summery.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('/')


def index(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'index.html',
                  context
                  )


def products(request):
    context = {
        'products': Product.objects.all()
    }

    return render(request, 'products.html',
                  context
                  )

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderInCart.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order is in the order
        if order.product.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "This item quantity is updated")
            return redirect("products:products", slug=slug)
        else:
            order.product.add(order_product)
            messages.info(request, "This item is added to your cart")
            return redirect("products:products", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.product.add(order_product)
        messages.info(request, "This item is added to your cart")
        return redirect("products:products", slug=slug)

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order is in the order
        if order.product.filter(product__slug=product.slug).exists():
            order_product = OrderInCart.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.product.remove(order_product)
            messages.info(request, "This item is removed from your cart")
            return redirect("products:order_summery")
        else:
            # print message user doesn't have an oder
            messages.info(request, "This item is not exist in your cart")
            return redirect("products:products", slug=slug)

    else:
        # print message user doesn't have an oder
        messages.info(request, "This item is not exist in your cart")
        return redirect("products:products", slug=slug)


@login_required
def add_single_product_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderInCart.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order is in the order
        if order.product.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "This item quantity is updated")
            return redirect("products:order_summery")
        else:
            order.product.add(order_product)
            messages.info(request, "This item is added to your cart")
            return redirect("products:order_summery")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.product.add(order_product)
        messages.info(request, "This item is added to your cart")
        return redirect("products:order-summery")


@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order is in the order
        if order.product.filter(product__slug=product.slug).exists():
            order_product = OrderInCart.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.product.remove(order_product)
            messages.info(request, "This item quantity is updated ")
            return redirect("products:order_summery")
        else:
            # print message user doesn't have an oder
            messages.info(request, "This item is not exist in your cart")
            return redirect("products:order_summery")

    else:
        # print message user doesn't have an oder
        messages.info(request, "This item is not exist in your cart")
        return redirect("products:order-summery")


class CheckoutView(View):
    def get(self, args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, 'checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You don't have an active order")
            return redirect('products:checkout')
        # form

    def post(self, args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                address_line_1 = form.cleaned_data.get('address_line_1')
                address_line_2 = form.cleaned_data.get('address_line_2')
                country = form.cleaned_data.get('country')
                state = form.cleaned_data.get('state')
                pin_code = form.cleaned_data.get('pin_code')
                """
                same_shipping_address = form.cleaned_data.get('same_shipping_address')
                save_info = form.cleaned_data.get('save_info')
                """
                billing_address = BillingAddress(
                    user=self.request.user,
                    address_line_1=address_line_1,
                    address_line_2=address_line_2,
                    country=country,
                    state=state,
                    pin_code=pin_code
                )
                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user=self.request.user,
                    address_line_1=address_line_1,
                    address_line_2=address_line_2,
                    country=country,
                    pin_code=pin_code,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # redirected to selected payment option

                # update the order after payment
                order_items = order.product.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                if payment_option == 'C':
                    return redirect('products:payment', payment_option='Credit Card')
                elif payment_option == 'D':
                    return redirect('products:payment', payment_option='Debit Card')
                elif payment_option == 'N':
                    return redirect('products:payment', payment_option='Net Banking')
                else:
                    messages.warning(self.request, "Invalid payment option selected.")
                    return redirect('products:checkout')

            messages.warning(self.request, "failed checkout")
            return redirect('products:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('products:order_summery')


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, "Please provide a valid billing address")
            return redirect('products:checkout')


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon is not valid")
        return redirect('products:checkout')


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Coupon is applied")
                return redirect('products:checkout')
            except ObjectDoesNotExist:
                messages.info(self.request, "You don't have an active order")
                return redirect('products:checkout')

