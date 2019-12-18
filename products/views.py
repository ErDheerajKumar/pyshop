from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderInCart, Address, Coupon, Returns
from django.views.generic import ListView, DetailView, View
from django.views.generic import ListView
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, ReturnForm
import random
import string


def create_order_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


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


def is_valid_form(values):
    valid = True
    for field in values:
        if field == " ":
            valid = False
    return valid


# @login_required
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
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update({'default_billing_address': billing_address_qs[0]})

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
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print('using default shipping address.')
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, "Default shipping address not available")
                        return redirect('products:checkout')
                else:
                    print("User is enter a new shipping address.")
                    shipping_address_1 = form.cleaned_data.get('shipping_address_1')
                    print(shipping_address_1)
                    shipping_address_2 = form.cleaned_data.get('shipping_address_2')
                    print(shipping_address_2)
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shipping_state = form.cleaned_data.get('shipping_state')
                    shipping_city = form.cleaned_data.get('shipping_city')
                    shipping_pin_code = form.cleaned_data.get('shipping_pin_code')
                    if is_valid_form([shipping_address_1, shipping_country, shipping_state, shipping_city, shipping_pin_code]):
                        shipping_address = Address(
                            user=self.request.user,
                            address_line_1=shipping_address_1,
                            address_line_2=shipping_address_2,
                            country=shipping_country,
                            state=shipping_state,
                            city=shipping_city,
                            pin_code=shipping_pin_code,
                            address_type='S'
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request, "Please provide a valid shipping address")

                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print('using default billing address.')
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, "Default billing address not available")
                        return redirect('products:checkout')
                else:
                    print("User is enter a new billing address.")
                    billing_address_1 = form.cleaned_data.get('billing_address_1')
                    billing_address_2 = form.cleaned_data.get('billing_address_2')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_state = form.cleaned_data.get('billing_state')
                    billing_city = form.cleaned_data.get('billing_city')
                    billing_pin_code = form.cleaned_data.get('billing_pin_code')
                    if is_valid_form([billing_address_1, billing_country, billing_city, billing_pin_code]):
                        billing_address = Address(
                            user=self.request.user,
                            address_line_1=billing_address_1,
                            address_line_2=billing_address_2,
                            country=billing_country,
                            state=billing_state,
                            city=billing_city,
                            pin_code=billing_pin_code,
                            address_type='B'
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()
                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(self.request, "Please provide a valid billing address")
                # redirected to selected payment option
                payment_option = form.cleaned_data.get('payment_option')
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
        # TODO: assign order id after successful payment
        '''
        order.order_id = create_order_id()
        '''


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


class RequestReturnView(View):
    def get(self, *args, **kwargs):
        form = ReturnForm()
        context = {
            'form': form
        }
        return render(self.request, "request_return.html",context)

    def post(self, *args, **kwargs):
        form = ReturnForm(self.request.POST)
        if form.is_valid():
            order_id = form.cleaned_data.get('order_id')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
        # edit the order
        try:
            order = Order.objects.get(order_id=order_id)
            order.return_request = True
            order.save()

        # process return
            returns  = Returns()
            returns.order = order
            returns.reason = message
            returns.email = email
            returns.save()
            messages.info(self.request, "Return request has been submitted.")
            return redirect("products:request_return")

        except ObjectDoesNotExist:
            messages.info(self.request, "This order does not exist.")
            return redirect("products:request_return")


