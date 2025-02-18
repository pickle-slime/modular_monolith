from django.forms import BaseModelForm
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from core.shop_management.presentation.shop_management.session_helper import inject_session_dependencies

from typing import Any

from .forms import RegisterUserForm, LoginUserForm

from core.user_management.application.services.internal.user_management import AuthenticationRegisterUserService, AuthenticationLoginUserService
from core.user_management.infrastructure.repositories.user_management import DjangoUserRepository
from core.user_management.infrastructure.adapters.jwtoken import JWTokenAdapter
from core.utils.application.base_view_mixin import BaseViewMixin
from core.shop_management.infrastructure.repositories.shop_management import DjangoCategoryRepository
from core.cart_management.infrastructure.repositories.cart_management import DjangoWishlistRepository
from core.user_management.infrastructure.repositories.user_management import DjangoUserRepository
from core.utils.application.base_service import BaseTemplateService

from core.user_management.infrastructure.adapters.dj_password_hasher import DjangoPasswordHasherAdapter
from config import JWT_SECRET_KEY, ACCESS_JWTOKEN_EXPIRY, REFRESH_JWTOKEN_EXPIRY

class RegisterUser(CreateView, BaseViewMixin):
    form_class = RegisterUserForm
    service_class = AuthenticationRegisterUserService
    service_classes = {
        "template_service": BaseTemplateService,
    }
    adapter_classes = {
        "token_adapter": JWTokenAdapter,
    }
    service_args = {
        "template_service": {
            "category_repository": DjangoCategoryRepository(),
            "cart_repository": None,
            "wishlist_repository": DjangoWishlistRepository(),
            "user_repository": DjangoUserRepository(),
            "session_adapter": None,
        }
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
        return self.service.get_context_data(context)
    
    def form_valid(self, form: BaseModelForm) -> JsonResponse:
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
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
            #login(self.request, user)
            return JsonResponse({'status': 'succeed'})
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': f'{form.errors}'})
        return super().form_invalid(form)
    
    def get(self, request, *args, **kwargs):
        inject_session_dependencies(self, request)
        return super().get(request, *args, **kwargs)
    
class LoginUser(LoginView, BaseViewMixin):
    form_class = LoginUserForm
    service_class = AuthenticationLoginUserService
    service_classes = {
        "template_service": BaseTemplateService,
    }
    adapter_classes = {
        "token_adapter": JWTokenAdapter,
    }
    service_args = {
        "template_service": {
            "category_repository": DjangoCategoryRepository(),
            "cart_repository": None,
            "wishlist_repository": DjangoWishlistRepository(),
            "user_repository": DjangoUserRepository(),
            "session_adapter": None,
        }
    }
    adapter_args={
        "token_adapter": {
            "secret_key": JWT_SECRET_KEY,
            "access_token_expiry": ACCESS_JWTOKEN_EXPIRY,
            "refresh_token_expiry": REFRESH_JWTOKEN_EXPIRY,
        }
    }
    template_name = 'user_management/login.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.service.get_context_data(context)
    
    def form_valid(self, form):
        user = form.get_user()
        email = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password")
        #user.backend = 'user_management.backends.EmailBackend'
        refresh_token, access_token = self.service.authenticate(email, raw_password, DjangoPasswordHasherAdapter())
        user.backend = 'user_management.backends.EmailBackend'
        response = super().form_valid(form)
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
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
        inject_session_dependencies(self, request)
        return super().get(request, *args, **kwargs)
    
def logout_user(request):
    logout(request)
    request.jwt = {"authorized": False, "error": None, "new_access_token": None}
    response = redirect('home')
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
