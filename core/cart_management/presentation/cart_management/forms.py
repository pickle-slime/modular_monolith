from django import forms

class BaseProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.object_dto = kwargs.pop('object_dto', None)
        super().__init__(*args, **kwargs)

        if self.object_dto is not None:
            self._populate_product_fields()

    def _populate_product_fields(self):
        product_sizes = self.object_dto.sizes
        self.fields['size'].choices = [(option.pub_uuid, option.size) for option in product_sizes] if product_sizes else []
        self.fields['color'].choices = [(color, color) for color in self.object_dto.color] if self.object_dto.color else []

    def clean(self) -> dict:
        cleaned_data = super().clean()
        
        size_uuid = cleaned_data.get('size')
        product = self.object_dto  

        if size_uuid and self.object_dto:
            size_instance = self.object_dto.sizes
            if not size_instance:
                raise forms.ValidationError("The selected size is not available for this product.")
            cleaned_data['size'] = size_instance 
            cleaned_data['product'] = product
        return cleaned_data
    
    class Meta:
        abstract = True

class AddToCartForm(BaseProductForm):
    def __init__(self, *args, **kwargs):
        self.cart_uuid = kwargs.pop('cart_uuid', None)
        super().__init__(*args, **kwargs)
        if self.cart_uuid is not None and 'cart' in self.fields:
            self.fields['cart'].initial = self.cart_uuid

    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'size'}))
    color = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'color'}))
    qty = forms.IntegerField(widget=forms.NumberInput(attrs={'value': '1'}))

class AddToWishlistForm(BaseProductForm):
    def __init__(self, *args, **kwargs):
        self.wishlist_uuid = kwargs.pop('wishlist_uuid', None)
        super().__init__(*args, **kwargs)
        if self.wishlist_uuid is not None and 'wishlist' in self.fields:
            self.fields['wishlist'].initial = self.wishlist_uuid

    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'size'}))
    color = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'color'}), required=False)
    qty = forms.IntegerField(widget=forms.NumberInput(attrs={'value': '1'}), required=False)


