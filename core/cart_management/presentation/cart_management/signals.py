from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender="user_management.CustomUser")
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
        WishList.objects.create(customer=instance)


@receiver(post_save, sender=WishListOrderProduct)
@receiver(post_save, sender=CartOrderProduct)
def update_cart(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, WishListOrderProduct):
            item_collection = instance.wishlist
            WishList.objects.update_total_price_and_quantity(item_collection, price=instance.size.product.get_price_with_discount(), qty=instance.qty)
        elif isinstance(instance, CartOrderProduct):
            item_collection = instance.cart
            Cart.objects.update_total_price_and_quantity(item_collection, price=instance.size.product.get_price_with_discount(), qty=instance.qty)