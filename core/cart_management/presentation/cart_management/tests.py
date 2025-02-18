from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.shop_management.presentation.models import Product, Category, ProductSizes
from .models import CartOrderProduct, WishListOrderProduct

import json

class BaseItemCollectionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        # Set up common data
        cls.category = Category.objects.create(name="Sample Category")

        cls.seller = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123321123"
        )

        cls.product = Product.objects.create(
            name="Sample Product",
            slug="Sample-Product",  # Generate slug from name
            description="This is a sample product description.",
            details="Here are the details of the sample product.",
            brand="Brand Name",
            image="path/to/image.jpg",  # Replace with actual path to image
            price=99.99,
            discount=10,  # 10% discount
            color=["black", "white"],  # List of color choices
            in_stock=10,
            count_of_selled=0,
            category=cls.category,
            seller=cls.seller
        )

        cls.product_sizes = ProductSizes.objects.create(
            size='2x', length=2.00, width=2.00, height=2.00, weight=2.00, product_id=cls.product.pk
        )

    def setUp(self):
        self.client.login(username='testuser@example.com', password='password123321123')


class ItemCollectionViewTest(BaseItemCollectionViewTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # Additional setup specific to cart and wishlist order products
        cls.cart_order_product = CartOrderProduct.objects.create(
            color='black', qty=1, cart_id=cls.seller.cart.pk, size_id=cls.product_sizes.pk
        )
        cls.wishlist_order_product = WishListOrderProduct.objects.create(
            color='black', qty=1, wishlist_id=cls.seller.cart.pk, size_id=cls.product_sizes.pk
        )

    def test_delete_button_cart(cls):
        response = cls.client.put(reverse('delete_button_cart'))
        cls.assertEqual(response.status_code, 302)
        cls.assertRedirects(response, reverse('home'))

    def test_delete_button_cart_ajax(cls):
        response = cls.client.put(
            reverse('delete_button_cart'),
            data=json.dumps({
                'type': 'CartOrderProduct', 
                'item': cls.cart_order_product.pk,
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        cls.assertEqual(response.status_code, 200)
        cls.assertContains(response, 'qty')
        cls.assertContains(response, 'qty-2')
        cls.assertContains(response, 'subtotal')

    def test_delete_button_wishlist(cls):
        response = cls.client.put(reverse('delete_button_wishlist'))
        cls.assertEqual(response.status_code, 302)
        cls.assertRedirects(response, reverse('home'))

    def test_delete_button_wishlist_ajax(cls):
        response = cls.client.put(
            reverse('delete_button_wishlist'),
            data=json.dumps({
                'type': 'WishListOrderProduct', 
                'item': cls.wishlist_order_product.pk,
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        cls.assertEqual(response.status_code, 200)
        cls.assertContains(response, 'qty')
        cls.assertContains(response, 'qty-2')
        cls.assertContains(response, 'subtotal')


class ItemCollectionViewTest2(BaseItemCollectionViewTest):
    def test_add_to_cart(cls):
        response = cls.client.put(reverse('add_to_cart'))
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.json()['status'], 'error')

    def test_add_to_cart_ajax(cls):
        response = cls.client.put(
            reverse('add_to_cart'),
            data=json.dumps({
                'type-collection': 'CartOrderProduct',
                'color': 'black',
                'size': cls.product_sizes.pk,
                'qty': '1',
                'product': cls.product.pk,
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.json()['status'], 'success')

    def test_add_to_wishlist(cls):
        response = cls.client.put(reverse('add_to_wishlist'))
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.json()['status'], 'error')

    def test_add_to_wishlist_ajax(cls):
        response = cls.client.put(
            reverse('add_to_wishlist'),
            data=json.dumps({
                'type-collection': 'WishListOrderProduct', 
                'size': cls.product_sizes.pk,  
                'qty': '1', 
                'product': cls.product.pk,
            }),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        cls.assertEqual(response.status_code, 200)
        cls.assertEqual(response.json()['status'], 'success')
