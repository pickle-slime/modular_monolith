from django import forms
from core.order_management.presentation.order_management.models import *

# class CheckoutForm(forms.ModelForm):
    
#     class Meta:
#         model = BillingAddress
#         fields = ['first_name', 'last_name', 'address', 'city', 'state', 'country', 'zip_code', 'telephone']
    
#     first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}))
#     address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Address'}))
#     city = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'City'}))
#     state = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'State'}))
#     country = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Country'}))
#     zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'ZIP Code'}))
#     telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Telephone'}))

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'country', 'zip_code', 'telephone']
    
    common_attrs = {'class': 'input'}

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'First Name'}),
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'Last Name'}),
        max_length=30,
        required=True
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'Address'}),
        required=True
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'City'}),
        required=True
    )
    state = forms.CharField(
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'State'}),
        required=True
    )
    country = forms.CharField(
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'Country'}),
        required=True
    )
    zip_code = forms.CharField(
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'ZIP Code'}),
        required=True,
        max_length=10,
        error_messages={'max_length': 'ZIP code must be at most 10 characters.'}
    )
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={**common_attrs, 'placeholder': 'Telephone'}),
        required=True,
        max_length=15,
        error_messages={'max_length': 'Telephone number must be at most 15 characters.'}
    )

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not telephone.isdigit():
            raise forms.ValidationError("Telephone number must contain only digits.")
        return telephone

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code.isdigit():
            raise forms.ValidationError("ZIP code must contain only digits.")
        return zip_code