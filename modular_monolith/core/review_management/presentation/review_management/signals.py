from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProductRating

@receiver(post_save, sender='shop_management.Product')
def create_product_rating(sender, instance, created, **kwargs):
    if created:
        ProductRating.objects.create(product=instance)