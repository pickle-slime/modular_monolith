from typing import Any

from django.http import HttpRequest
from django.forms import BaseForm

from core.order_management.presentation.order_management.models import *

from core.utils.application.base_service import BaseService
from core.payment_management.application.services.external.payment_management import create_payment_intent
from ..external.order_management import ShippoService


class CheckoutService(BaseService):
    
    def get_context_data(self, request: HttpRequest, context: dict[str: Any]) -> dict[str: Any]:
        return {**self.get_header_and_footer(request), **context}
    
    
    def form_valid(self, request: HttpRequest, form: BaseForm):
        intent = self.create_payment_intent(request)
        order = self.create_order(request, intent)
        billing_address = self.save_billing_address(form, order)
        shipment_object = None
        
        try:
            shipment, transaction = self.create_shipment_transaction(request, billing_address)
            order.status = Order.SHIPPED
            shipment_object = self.save_shipment(order, shipment, transaction)
            order.save()

            # Pass client secret and order_id to context for the payment step
            return {
                'client_secret': intent['client_secret'],
                'order_id': order.id
            }
        except Exception as e:
            self.handle_form_valid_exception(order, shipment_object, billing_address)
            raise e

    def create_payment_intent(self, request: HttpRequest):
        return create_payment_intent(request.user.cart.total_price)

    def create_order(self, request: HttpRequest, intent: dict):
        return Order.objects.create(
            user=request.user,
            total_amount=request.user.cart.total_price,
            stripe_payment_intent_id=intent['id']
        )

    def save_billing_address(self, form: BaseForm, order: Order):
        billing_address = form.save(commit=False)
        billing_address.order = order
        billing_address.save()
        return billing_address

    def create_shipment_transaction(self, request: HttpRequest, billing_address):
        sender_address = self.get_sender_address()
        recipient_address = billing_address.to_shippo_address()
        list_of_parcels = Cart.objects.get_list_of_parcels(request.user.cart)

        # Create Shipment with Shippo
        shipment = ShippoService.create_shipment(sender_address, recipient_address, list_of_parcels)

        # Create Transaction with Shippo
        transaction = ShippoService.create_transaction(shipment)
        return shipment, transaction

    def save_shipment(self, order: Order, shipment, transaction):
        shipment = Shipment.objects.create(
            tracking_number=transaction.tracking_number,
            shipment_id=shipment.object_id,
            transaction_id=transaction.object_id,
            label_url=transaction.label_url,
            shipping_cost=shipment.rates[0].amount,
            order=order,
        )
        shipment.save()

        return shipment

    def handle_form_valid_exception(self, order: Order, shipment: Shipment, billing_address: BillingAddress):
        if order and order.pk:
            order.delete()  
        if shipment and shipment.pk: 
            shipment.delete()
        if billing_address and billing_address.pk: 
            billing_address.delete()

    def get_sender_address(self) -> dict:
        return {
            "name": "Shawn Ippotle",
            "email": "randomuser1234@example.com",
            "street1": "215 Clayton St.",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94117",
            "country": "US",
            "phone": "(555) 123-4567",
        }