import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from unittest.mock import patch

from user_management.views import RegisterUser
from user_management.forms import RegisterUserForm, AuthenticationForm


@pytest.fixture
def client_instance(client):
    return client

@pytest.fixture
def register_url():
    return reverse('register')

@pytest.fixture
def custom_user():
    return get_user_model()

@pytest.fixture
def login_url():
    return reverse('login')

@pytest.fixture
def user_instance(custom_user):
    return custom_user.objects.create_user(email='testuser@example.com', username='testuser', password='strongpassword')

@pytest.fixture
def logout_url():
    return reverse('logout')

@pytest.mark.django_db
def test_get_register_page(client_instance, register_url):
    response = client_instance.get(register_url)
    assert response.status_code == 200
    assert 'user_management/register.html' in (t.name for t in response.templates)

@pytest.mark.django_db
def test_post_register_access(client_instance, register_url, custom_user):
    response = client_instance.post(register_url, {
        'username': 'testuser',
        'password1': 'strongpassword',
        'password2': 'strongpassword',
        'email': 'testuser@example.com'
    })
    assert custom_user.objects.filter(email='testuser@example.com').exists()
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_post_register_invalid(client_instance, register_url):
    """Test form submission with invalid data (passwords don't match)."""
    response = client_instance.post(register_url, {
        'username': 'testuser',
        'password1': 'password123',
        'password2': 'wrongpassword',
        'email': 'testuser@example.com'
    })
    assert response.status_code == 200
    assert 'user_management/register.html' in (t.name for t in response.templates)
    form = response.context['form']
    assert form.errors['password2'] == ['The two password fields didn’t match.']

@pytest.mark.django_db
def test_ajax_post_register_success(client_instance, register_url, custom_user):
    """Test successful AJAX form submission."""
    response = client_instance.post(register_url, {
        'username': 'testuser',
        'password1': 'strongpassword',
        'password2': 'strongpassword',
        'email': 'testuser@example.com'
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert response.status_code == 200
    assert isinstance(response, JsonResponse)
    assert response.json() == {'status': 'succeed'}
    assert custom_user.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_ajax_post_register_failure(client_instance, register_url, custom_user):
    """Test failed AJAX form submission."""
    response = client_instance.post(register_url, {
        'username': 'testuser',
        'password1': 'password123',
        'password2': 'wrongpassword',
        'email': 'testuser@example.com'
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert response.status_code == 200
    assert isinstance(response, JsonResponse)
    assert 'status' in response.json()
    assert not custom_user.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_register_user_context(client_instance, register_url):
    """Test that the get_context_data method is called."""
    response = client_instance.get(register_url)

    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], RegisterUserForm)


@pytest.mark.django_db
def test_get_login_page(client_instance, login_url):
    """Test GET request to load the login page."""
    response = client_instance.get(login_url)
    assert response.status_code == 200
    assert 'user_management/login.html' in (t.name for t in response.templates)

@pytest.mark.django_db
def test_post_login_success(client_instance, login_url, user_instance):
    """Test successful login."""
    response = client_instance.post(login_url, {
        'username': 'testuser@example.com',
        'password': 'strongpassword',
    })
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_post_login_failure(client_instance, login_url):
    """Test login with incorrect credentials."""
    response = client_instance.post(login_url, {
        'username': 'testuser@exxample.com',
        'password': 'wrongpassword',
    })
    assert response.status_code == 200
    assert 'user_management/login.html' in (t.name for t in response.templates)
    form = response.context['form']
    assert form.errors["__all__"] == ['Please enter a correct email address and password. Note that both fields may be case-sensitive.']

@pytest.mark.django_db
def test_context_data(client_instance, login_url):
    """Test that context data is correctly populated."""
    response = client_instance.get(login_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], AuthenticationForm)

@pytest.mark.django_db
@patch("user_management.views.LoginUser.get_context_data")
def test_login_user_context(mock_context_data, client_instance, login_url):
    """Test that the get_context_data method is called."""
    mock_context_data.return_value = {'key': 'value'}
    response = client_instance.get(login_url)
    mock_context_data.assert_called_once()
    assert 'key' in response.context
    assert response.context['key'] == 'value'


@pytest.mark.django_db
def test_logout_user(client_instance, user_instance, logout_url):
    """Test user logout."""
    client_instance.login(username='testuser', password='strongpassword')
    response = client_instance.get(logout_url)
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert '_auth_user_id' not in client_instance.session
