from django.db import models
from django.urls import reverse

from .managers import ProductRatingManager

import uuid

class ProductRating(models.Model):
    inner_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    public_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, editable=False, null=True)
    product = models.OneToOneField('shop_management.Product', on_delete=models.CASCADE, related_name='product_rating')

    #objects = ProductRatingManager()


class Review(models.Model):
    '''
    Model of reviews for products
    '''
    inner_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    public_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("user_management.CustomUser", on_delete=models.CASCADE)
    product_rating = models.ForeignKey(ProductRating, on_delete=models.CASCADE, related_name='reviews')

    def get_absolute_url(self):
        return reverse('review', kwargs={'category': self.product.category.slug, 'product': self.product.slug})

    def delete(self, *args, **kwargs):
        ProductRating.objects.update_rating(self.product_rating)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ProductRating.objects.update_rating(self.product_rating)
 
