from django.forms import BaseModelForm
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from core.utils.presentation.session_helper import inject_session_dependencies_into_view
from core.utils.infrastructure.adapters.dj_url_mapping import DjangoURLAdapter

from typing import Any

from .forms import RegisterUserForm, LoginUserForm

from core.user_management.application.services.internal.user_management import AuthenticationRegisterUserService, AuthenticationLoginUserService
from core.user_management.infrastructure.repositories.user_management import DjangoUserRepository
from core.user_management.infrastructure.adapters.jwtoken import JWTokenAdapter
from core.utils.application.base_view_mixin import BaseViewMixin
from core.shop_management.presentation.acl_factory import ShopManagementACLFactory
from core.shop_management.presentation.shop_management.forms import SearchForm
from core.cart_management.presentation.acl_factory import CartManagementACLFactory

from core.user_management.infrastructure.adapters.dj_password_hasher import DjangoPasswordHasherAdapter
from config import JWT_SECRET_KEY, ACCESS_JWTOKEN_EXPIRY, REFRESH_JWTOKEN_EXPIRY

class RegisterUser(CreateView, BaseViewMixin):
    form_class = RegisterUserForm
    service_class = AuthenticationRegisterUserService
    service_classes = {
        "category_acl": ShopManagementACLFactory.create_category_acl(),
        "cart_acl": None,
        "wishlist_acl": CartManagementACLFactory.create_wishlist_acl(),
    }
    adapter_classes = {
        "token_adapter": JWTokenAdapter,
        "session_adapter": None,
        "url_mapping_adapter": DjangoURLAdapter,
    }
    repository_classes = {
        "user_repository": DjangoUserRepository,
    }
    adapter_args = {
        "token_adapter": {
            "secret_key": JWT_SECRET_KEY,
            "access_token_expiry": ACCESS_JWTOKEN_EXPIRY,
            "refresh_token_expiry": REFRESH_JWTOKEN_EXPIRY,
        }
    }
    template_name = 'user_management/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        service_context = self.service.get_context_data(context)
        service_context["search_bar"] = SearchForm(categories=service_context["search_bar"])
        return service_context
    
    def form_valid(self, form: BaseModelForm):
        if self.request.method == 'POST':
            user = form.save()
            email = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            refresh_token, access_token = self.service.authenticate(email, raw_password, DjangoPasswordHasherAdapter())
            user.backend = 'user_management.backends.EmailBackend'
            response = super().form_valid(form)
            response.set_cookie(
                "refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Strict"
            )
            self.request.new_access_token = access_token
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        if self.request.method == 'POST':
            return JsonResponse({'status': 'error', 'message': f'{form.errors}'})
        return super().form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        inject_session_dependencies_into_view(self, request)
        return super().get(request, *args, **kwargs)
    
class LoginUser(LoginView, BaseViewMixin):
    form_class = LoginUserForm
    service_class = AuthenticationLoginUserService
    service_classes = {
        "category_acl": ShopManagementACLFactory.create_category_acl(),
        "cart_acl": None,
        "wishlist_acl": CartManagementACLFactory.create_wishlist_acl(),
    }
    adapter_classes = {
        "token_adapter": JWTokenAdapter,
        "session_adapter": None,
        "url_mapping_adapter": DjangoURLAdapter,
    }
    repository_classes = {
        "user_repository": DjangoUserRepository,
    }
    adapter_args = {
        "token_adapter": {
            "secret_key": JWT_SECRET_KEY,
            "access_token_expiry": ACCESS_JWTOKEN_EXPIRY,
            "refresh_token_expiry": REFRESH_JWTOKEN_EXPIRY,
        }
    }
    template_name = 'user_management/login.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        service_context = self.service.get_context_data(context)
        service_context["search_bar"] = SearchForm(categories=service_context["search_bar"])
        return service_context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.method == 'POST':
            user = form.get_user()
            email = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            refresh_token, access_token = self.service.authenticate(email, raw_password, DjangoPasswordHasherAdapter())
            user.backend = 'user_management.backends.EmailBackend'
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Strict"
            )
            self.request.new_access_token = access_token
            login(self.request, user)
        return response

    def form_invalid(self, form: BaseModelForm):
        if self.request.method == 'POST':
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
        inject_session_dependencies_into_view(self, request)
        return super().get(request, *args, **kwargs)
    
def logout_user(request):
    logout(request)
    request.jwt = {"authorized": False, "error": None, "new_access_token": None}
    response = redirect('home')
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
