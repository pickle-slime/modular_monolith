from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from unittest.mock import patch

from .forms import RegisterUserForm, LoginUserForm
from .views import RegisterUser


#VIEW TEST CASES

class RegisterUserViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
        self.custom_user = get_user_model()

    def test_get_register_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management/register.html')

    def test_post_register_access(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password1': 'strongpassword',
            'password2': 'strongpassword',
            'email': 'testuser@example.com'
        })
        self.assertTrue(self.custom_user.objects.filter(email='testuser@example.com').exists())
        self.assertRedirects(response, reverse('home'))

    def test_post_register_invalid(self):
        """Test form submission with invalid data (passwords don't match)."""
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'wrongpassword',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed("user_management/register.html")

        form = response.context['form']
        self.assertFormError(form, 'password2', 'The two password fields didn’t match.')

    def test_ajax_post_register_success(self):
        """Test successful AJAX form submission."""
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password1': 'strongpassword',
            'password2': 'strongpassword',
            'email': 'testuser@example.com'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertJSONEqual(response.content, {'status': 'succeed'})
        self.assertTrue(self.custom_user.objects.filter(username='testuser').exists())

    def test_ajax_post_register_failure(self):
        """Test failed AJAX form submission."""
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'wrongpassword',
            'email': 'testuser@example.com'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertIn('status', response.json())
        self.assertFalse(self.custom_user.objects.filter(username='testuser').exists())

    @patch('user_management.views.RegisterUser.get_context_data')
    def test_register_user_context(self, mock_context_data):
        """Test that the get_context_data method is called."""
        mock_context_data.return_value = {'form': RegisterUserForm, 'view': RegisterUser}
        response = self.client.get(reverse('register'))
        mock_context_data.assert_called_once()
        self.assertIn('form', response.context)
        self.assertIn('view', response.context)
    

class LoginUserViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='strongpassword')

    def test_get_login_page(self):
        """Test GET request to load the login page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management/login.html')

    def test_post_login_success(self):
        """Test successful login."""
        response = self.client.post(self.url, {
            'username': 'testuser@example.com',
            'password': 'strongpassword',
        })
        self.assertRedirects(response, reverse('home'))

    def test_post_login_failure(self):
        """Test login with incorrect credentials."""
        response = self.client.post(self.url, {
            'username': 'testuser@exxample.com',
            'password': 'wrongpassword',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('user_management/login.html')

        form = response.context['form']
        self.assertFormError(form, None, 'Please enter a correct email address and password. Note that both fields may be case-sensitive.')

    def test_context_data(self):
        """Test that context data is correctly populated."""
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    @patch("user_management.views.LoginUser.get_context_data")
    def test_login_user_context(self, mock_context_data):
        """Test that the get_context_data method is called."""
        mock_context_data.return_value = {'key': 'value'}
        response = self.client.get(reverse('login'))
        mock_context_data.assert_called_once()
        self.assertIn('key', response.context)
        self.assertTrue(response.context['key'] == 'value')

class LogoutUserViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='strongpassword')

    def test_logout_user(self):
        """Test user logout."""
        self.client.login(username='testuser', password='strongpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)


#FORM TEST CASES


class RegisterUserFormTests(TestCase):

    def test_valid_form(self):
        form_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123321123',
            'password2': 'password123321123',
        }
        form = RegisterUserForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        form_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'differentpassword',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_missing_fields(self):
        form_data = {
            'email': '',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class LoginUserFormTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='password123321123',
            first_name='Test',
            last_name='User',
        )

    def test_valid_form(self):
        form_data = {
            'username': 'test@example.com', 
            'password': 'password123321123',
        }
        form = LoginUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_fields(self):
        form_data = {
            'username': '',
            'password': 'password123',
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_invalid_email_format(self):
        form_data = {
            'username': 'invalid-email',
            'password': 'password123',
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


#MODEL TEST CASES


class CustomUserTests(TestCase):

    def setUp(self):
        self.User = get_user_model()  # Get the custom user model
        self.user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123321123'
        )

    def test_create_user(self):
        # Check if the user is created correctly
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('password123321123'))
        self.assertEqual(self.user.username, 'testuser')

    def test_create_user_without_email(self):
        # Test that creating a user without an email raises a ValueError
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='testuser')

    def test_create_superuser(self):
        # Create a superuser and check its properties
        superuser = self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password('adminpassword'))

    def test_superuser_without_is_staff(self):
        # Test that creating a superuser without is_staff raises a ValueError
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword',
                is_staff=False
            )

    def test_superuser_without_is_superuser(self):
        # Test that creating a superuser without is_superuser raises a ValueError
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword',
                is_superuser=False
            )

    def test_user_str_method(self):
        # Test the string representation of the user
        self.assertEqual(str(self.user), 'testuser')