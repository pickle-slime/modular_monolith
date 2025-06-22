from django.urls import path
from .views import *

urlpatterns = [
    path('config/', stripe_config, name='stripe_config'),
    path('payment-intent/', payment_intent, name='payment_intent'),
]
