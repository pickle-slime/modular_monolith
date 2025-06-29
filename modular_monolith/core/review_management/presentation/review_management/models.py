from django.db import models
from django.urls import reverse

import uuid

class ProductRating(models.Model):
    inner_uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    public_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, editable=False, null=True)
    product = models.OneToOneField('shop_management.Product', on_delete=models.CASCADE, related_name='product_rating')

class Review(models.Model):
    '''
    Model of reviews for products
    '''
    inner_uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    public_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("user_management.CustomUser", on_delete=models.CASCADE, to_field="public_uuid")
    product_rating = models.ForeignKey(ProductRating, on_delete=models.CASCADE, related_name='reviews')

    def get_absolute_url(self):
        return reverse('review', kwargs={'category': self.product_rating.product.category.slug, 'product': self.product_rating.product.slug})
