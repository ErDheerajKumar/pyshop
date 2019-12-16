from django import forms

COUNTRY_CHOICES = (
    ('', 'Choose'),
    ('IN', 'India')
)
STATE_CHOICES = (
    ('', 'Choose'),
    ('RJ', 'Rajasthan')
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
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'House no. , colony',
        'class': 'form-control'
    }))
    address_line_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': "Apartment or Landmark",
        'class': 'form-control'
    }))
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    state = forms.ChoiceField(choices=STATE_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    pin_code = forms.ChoiceField(choices=PIN_CHOICES, widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    same_shipping_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria - label': 'Recipient\'s username',
        'aria - describedby': 'basic-addon2'
    }))

