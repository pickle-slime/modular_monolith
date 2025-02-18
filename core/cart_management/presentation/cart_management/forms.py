from django import forms

from .models import CartOrderProduct, WishListOrderProduct

class BaseProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.object_entity = kwargs.pop('object_entity', None)
        super().__init__(*args, **kwargs)

        if self.object_entity is not None:
            self._populate_product_fields()

    def _populate_product_fields(self):
        product_sizes = self.object_entity.product_sizes
        self.fields['size'].choices = [(option.uuid, option.size) for option in product_sizes] if product_sizes else []
        self.fields['color'].choices = [(color, color) for color in self.object_entity.color] if self.object_entity.color else []

    def clean(self):
        cleaned_data = super().clean()
        
        size_uuid = cleaned_data.get('size')
        product = self.object_entity  

        if size_uuid and self.object_entity:
            #size_instance = ProductSizes.objects.get(id=size_uuid, product=product) 
            size_instance = self.object_entity.sizes
            if not size_instance:
                raise forms.ValidationError("The selected size is not available for this product.")
            cleaned_data['size'] = size_instance 
            cleaned_data['product'] = product
    
    class Meta:
        abstract = True

class AddToCartForm(BaseProductForm):
    def __init__(self, *args, **kwargs):
        self.cart_pk = kwargs.pop('cart_pk', None)
        super().__init__(*args, **kwargs)
        if self.cart_pk is not None and 'cart' in self.fields:
            self.fields['cart'].initial = self.cart_pk

    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'size'}))
    color = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'color'}))
    qty = forms.IntegerField(widget=forms.NumberInput(attrs={'value': '1'}))

    class Meta:
        model = CartOrderProduct
        fields = ['size', 'color', 'qty', 'cart']

class AddToWishlistForm(BaseProductForm):
    def __init__(self, *args, **kwargs):
        self.wishlist_pk = kwargs.pop('wishlist_pk', None)
        super().__init__(*args, **kwargs)
        if self.wishlist_pk is not None and 'wishlist' in self.fields:
            self.fields['wishlist'].initial = self.wishlist_pk

    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'size'}))
    color = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'color'}), required=False)
    qty = forms.IntegerField(widget=forms.NumberInput(attrs={'value': '1'}), required=False)

    class Meta:
        model = WishListOrderProduct
        fields = ['size', 'color', 'qty', 'wishlist']
