from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth import get_user_model
from .models import CommonMailingList 
import requests

User = get_user_model()

class NewsletterIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.client.login(username='testuser@example.com', password='password123')
        self.url = reverse('newsletter')

    @patch('notification_management.services.services.subscribe_user_to_mailchimp') 
    def test_newsletter_successful_subscription(self, mock_subscribe_user):
        # Mock the Mailchimp API response
        mock_subscribe_user.return_value = (200, {"status": "success", "message": "You have been subscribed successfully."})

        # Simulate an AJAX POST request with valid email
        response = self.client.post(
            self.url,
            data={
                "email": "testuser@example.com",
                "Fname": "John",
                "Lname": "Doe"
            },
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Assert Mailchimp API was called once
        mock_subscribe_user.assert_called_once_with(email="testuser@example.com", first_name="John", last_name="Doe")

        # Assert response status and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

        # Assert that the user was added to the CommonMailingList
        self.assertTrue(CommonMailingList.objects.filter(email="testuser@example.com", user=self.user).exists())

    @patch('notification_management.services.services.subscribe_user_to_mailchimp')
    def test_newsletter_invalid_email(self, mock_subscribe_user):
        # Simulate an AJAX POST request with an invalid email
        response = self.client.post(
            self.url,
            data={
                "email": "wrongemail@example.com",  # Wrong email
                "Fname": "John",
                "Lname": "Doe"
            },
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Assert Mailchimp API was not called due to the incorrect email
        mock_subscribe_user.assert_not_called()

        # Assert response status and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")
        self.assertEqual("Incorrect email address: wrongemail@example.com", response.json()["message"])

    def test_non_ajax_post_redirects(self):
        # Simulate a non-AJAX POST request
        response = self.client.post(self.url, data={"email": "testuser@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    @patch('notification_management.services.services.subscribe_user_to_mailchimp')  # Adjust to your actual app name
    def test_newsletter_missing_email(self, mock_subscribe_user):
        # Simulate an AJAX POST request with missing email
        response = self.client.post(
            self.url,
            data={"Fname": "John", "Lname": "Doe"},  # Missing email field
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        mock_subscribe_user.assert_not_called()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")

    def test_newsletter_invalid_json(self):
        # Simulate an AJAX POST request with invalid JSON data
        response = self.client.post(
            self.url,
            data="invalid_json_string",  # Invalid JSON format
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")

    @patch('notification_management.services.services.subscribe_user_to_mailchimp')
    def test_mailchimp_timeout(self, mock_subscribe_user):
        # Mock a timeout exception from Mailchimp
        mock_subscribe_user.side_effect = requests.exceptions.Timeout

        response = self.client.post(
            self.url,
            data={
                "email": "testuser@example.com",
                "Fname": "John",
                "Lname": "Doe"
            },
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 504)
        self.assertEqual(response.json()["status"], "error")
        self.assertIn("timed out", response.json()["message"])

    def test_newsletter_unauthenticated_user(self):
        # Simulate an unauthenticated user request
        self.client.logout()  # Log the user out to simulate unauthenticated request
        response = self.client.post(
            self.url,
            data={
                "email": "testuser@example.com",
                "Fname": "John",
                "Lname": "Doe"
            },
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 401)  # Redirect to login or appropriate page