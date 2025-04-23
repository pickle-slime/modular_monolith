from django import forms

class ReviewForm(forms.Form):
    text = forms.CharField(max_length=500, required=True)
    rating = forms.IntegerField(min_value=1, max_value=5, required=True)
    product_rating = forms.UUIDField(required=True)
    user = forms.UUIDField(required=True)
