from django import forms
from .models import ShippingDetails, PaymentDetails, ProductReview


class ShippingDetailsForm(forms.ModelForm):
    class Meta:
        model = ShippingDetails
        exclude = ["csrfmiddlewaretoken", "user"]


class PaymentDetailsForm(forms.ModelForm):
    class Meta:
        model = PaymentDetails
        exclude = ["csrfmiddlewaretoken", "user"]


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        exclude = ["csrfmiddlewaretoken", "name"]


class PriceRangeForm(forms.Form):
    min_price = forms.DecimalField(label='Minimum Price', min_value=0)
    max_price = forms.DecimalField(label='Maximum Price', min_value=0)
