from django.urls import path

from .views import *

urlpatterns = [
    path('home/ajax-delete-button-cart/', delete_button_cart, name='delete_button_cart'),
    path('home/ajax-delete-button-wishlist/', delete_button_wishlist, name='delete_button_wishlist'),
    path('home/add-to-wishlist/', add_to_wishlist, name="add_to_wishlist"),
    path('home/add-to-cart/', add_to_cart, name="add_to_cart"),
]
