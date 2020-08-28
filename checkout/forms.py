from django import forms
from .models import BillingAddress


class BillingForm(forms.ModelForm):
    pincode = forms.IntegerField(min_value=100000, max_value=999999)
    landmark = forms.CharField(required=False, max_length=30)

    class Meta:
        model = BillingAddress
        fields = ["address", "pincode", "city", "landmark"]
