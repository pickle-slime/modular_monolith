from django.contrib import admin

from .models import *

admin.site.register(BillingAddress)
admin.site.register(Shipment)
admin.site.register(Order)
