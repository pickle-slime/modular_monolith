from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from .models import Order, Shipment
from django.conf import settings

from shippo.models import components
import shippo

User = get_user_model()

class CheckoutPageIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser@example.com', password='testpassword')

        self.url = reverse('checkout')


        # shippo_api_key = shippo.Shippo(api_key_header=settings.SHIPPO_API_KEY)

        # shipment = shippo_api_key.shipments.create(
        #     components.ShipmentCreateRequest(
        #         address_from=components.AddressCreateRequest(**from_address),
        #         address_to=components.AddressCreateRequest(**to_address),
        #         parcels=parcels,#[components.ParcelCreateRequest(**parcel)],
        #         async_=False
        #     )
        # )

        # rate = shipment.rates[0]

        # transaction = shippo_api_key.transactions.create(
        #     components.TransactionCreateRequest(
        #         rate=rate.object_id,
        #         label_file_type=components.LabelFileType.PDF,
        #         async_=False
        #     )
        # )

    @patch('payment_management.services.stripe_service.create_payment_intent')
    @patch('order_management.services.shippo_services.ShippoService.create_shipment')
    @patch('order_management.services.shippo_services.ShippoService.create_transaction')
    def test_checkout_valid_ajax_form_submission(self, mock_create_transaction, mock_create_shipment, mock_create_payment_intent):
        # Mock responses for payment and shipment services
        mock_create_payment_intent.return_value = {'id': 'pi_test', 'client_secret': 'secret_test'}
        mock_create_shipment.return_value = {'object_id': 'shipment_id'}
        mock_create_transaction.return_value = {'tracking_number': 'tracking_number', 'label_url': 'label_url'}

        # Create a valid checkout form data
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'city': 'San Francisco',
            'state': 'CA',
            'country': 'US',
            'zip_code': '94105',     
            'telephone': '071123456789'
        }

        response = self.client.post(self.url, data=form_data, #content_type='application/json', 
                                     HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'succeed')

        # Check that an order was created
        order = Order.objects.last()
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)

        # Check that the shipment was created
        shipment = Shipment.objects.last()
        self.assertIsNotNone(shipment)
        self.assertEqual(shipment.order, order)

    def test_checkout_invalid_form(self):
        invalid_form_data = {
            'address': '',  # Empty address to trigger form validation error
            'city': 'Test City',
            'state': 'CA',
            'zip_code': '12345',
            'country': 'US',
        }

        response = self.client.post(self.url, data=invalid_form_data, content_type='application/json',
                                     HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertIn('address', response.json()['message'])

    def test_checkout_unauthenticated_user(self):
        # Log out the user to simulate an unauthenticated request
        self.client.logout()

        response = self.client.get(self.url)

        # Since it's a GET request and the user is unauthenticated,
        # it should redirect to the login URL
        expected_redirect_url = f"{reverse("login")}?next={self.url}"
        self.assertRedirects(response, expected_redirect_url)
