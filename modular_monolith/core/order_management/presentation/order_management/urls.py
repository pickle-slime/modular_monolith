from django.urls import path
from .views import *

urlpatterns = [
    path('home/checkout/', CheckoutPage.as_view(), name='checkout'),
]
