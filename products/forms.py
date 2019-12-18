from django import forms

COUNTRY_CHOICES = (
    ('', 'Choose'),
    ('IN', 'India')
)
STATE_CHOICES = (
    ('', 'Choose'),
    ('RJ', 'Rajasthan')
)
CITY_CHOICES = (
    ('', 'Choose'),
    ('BHL', 'Bhilwara')
)
PIN_CHOICES = (
    ('', 'Choose'),
    ('311001', '311001')
)
PAYMENT_CHOICES = (
    ('C', 'Credit Card'),
    ('D', 'Debit Card'),
    ('N', 'Net Banking')
)


class CheckoutForm(forms.Form):
    shipping_address_1 = forms.CharField(required=False)
    shipping_address_2 = forms.CharField(required=False)
    shipping_country = forms.ChoiceField(required=False, choices=COUNTRY_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    shipping_state = forms.ChoiceField(required=False, choices=STATE_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    shipping_city = forms.ChoiceField(required=False, choices=CITY_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    shipping_pin_code = forms.ChoiceField(required=False, choices=PIN_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))

    billing_address_1 = forms.CharField(required=False)
    billing_address_2 = forms.CharField(required=False)
    billing_country = forms.ChoiceField(required=False, choices=COUNTRY_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    billing_state = forms.ChoiceField(required=False, choices=STATE_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    billing_city = forms.ChoiceField(required=False, choices=CITY_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    billing_pin_code = forms.ChoiceField(required=False, choices=PIN_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))

    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    set_default_shipping = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    use_default_shipping = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    set_default_billing = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    use_default_billing = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria - label': 'Recipient\'s username',
        'aria - describedby': 'basic-addon2'
    }))


class ReturnForm(forms.Form):
    order_id = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
                                                    'rows': 5
                                                    }))
    email = forms.EmailField()
