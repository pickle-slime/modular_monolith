from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from core.shop_management.infrastructure.repositories.shop_management import DjangoBrandRepository, DjangoCategoryRepository

from core.shop_management.presentation.shop_management.models import *
 
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Search here'}))
    category = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class': 'input-select'}))

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(0, 'category')] + [(cat.uuid, cat.name) for cat in categories]

class FiltersAside(forms.Form):
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)
    brand = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)
    price__min = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'price-min', 'type': 'number'}))
    price__max = forms.IntegerField(widget=forms.NumberInput(attrs={'id': 'price-max', 'type': 'number'}))
    sort_by = forms.ChoiceField(choices=(('1', 'Popular'), ('2', 'Price'), ('3', 'Hot Deals'),), widget=forms.Select(attrs={'class': 'input-select'}))


    _categories_cache = None
    _brands_cache = None

    def __init__(self, *args, **kwargs):
        super(FiltersAside, self).__init__(*args, **kwargs)

        self.fields['category'].choices = self._get_category_choices()
        self.fields['brand'].choices = self._get_brand_choices()

    @staticmethod
    def _get_category_choices():
        categories = DjangoCategoryRepository.fetch_categories_for_form(limit=6)
        return [(str(category.public_uuid), category.name) for category in categories]

    @staticmethod
    def _get_brand_choices():
        brands = DjangoBrandRepository.fetch_brands_for_form(limit=6)
        return [(str(brand.public_uuid), brand.name) for brand in brands]
    
    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get('price__min')
        price_max = cleaned_data.get('price__max')
        sort_by = cleaned_data.get('sort_by', 1)

        sort_mapping = {
            '1': 'count_of_selled',
            '2': 'price',
            '3': '-time_updated',
        }

        for key in sort_by:
            if key in sort_mapping:
                sort_by = sort_mapping[key]
                break

        cleaned_data['sort_by'] = sort_by

        if price_min is not None and price_max is not None and price_min > price_max:
            raise forms.ValidationError("Minimum price cannot be greater than maximum price.")
        return cleaned_data
