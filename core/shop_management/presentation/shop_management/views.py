from typing import Any

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect

from core.shop_management.presentation.shop_management.session_helper import inject_session_dependencies

from .forms import *
from .models import Product
from core.shop_management.application.services.internal.shop_management import *

from core.utils.application.base_view_mixin import BaseViewMixin
from core.utils.application.base_factories import BaseServiceFactory
from core.shop_management.infrastructure.repositories.shop_management import DjangoProductRepository, DjangoCategoryRepository, DjangoBrandRepository, DjangoProductImagesRepository
from core.cart_management.presentation.cart_management.forms import AddToCartForm, AddToWishlistForm
from core.cart_management.presentation.acl_factory import CartManagementACLFactory
from core.user_management.presentation.acl_factory import UserManagementACLFactory
from core.review_management.infrastructure.repositories.review_management import DjangoProductRatingRepository, DjangoReviewRepository, DjangoReviewReadModel
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.utils.infrastructure.adapters.dj_url_mapping import DjangoURLAdapter
from ...application.services.base_service import BaseTemplateService

SERVICE_FACTORY = BaseServiceFactory(
    services={
        "cart_acl": None,
        "wishlist_acl": CartManagementACLFactory.create_wishlist_acl(),
        "user_acl": UserManagementACLFactory.create_user_acl(),
    },
    repositories={
        "category_repository": DjangoCategoryRepository,
        "product_repository": DjangoProductRepository,
        "brand_repository": DjangoBrandRepository,
        "product_images_repository": DjangoProductImagesRepository,
    },
    adapters={
        "url_mapping_adapter": DjangoURLAdapter,
        "session_adapter": None
    }
)

class HomePage(ListView, BaseViewMixin):
    model = Product
    service_class = HomePageService
    service_factory = SERVICE_FACTORY
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        service_context = self.service.get_context_data()
        service_context["search_bar"] = SearchForm(categories=service_context["search_bar"])
        return {**context, **service_context}
    
    def dispatch(self, request, *args, **kwargs):
        inject_session_dependencies(self, request)
        return super().dispatch(request, *args, **kwargs)
    

class StorePage(ListView, FormMixin, BaseViewMixin):
    model = Product
    service_class = StorePageService
    service_factory = SERVICE_FACTORY
    template_name = 'shop/store.html'
    slug_url_kwargs = 'category'
    paginate_by = 9
    form_class = FiltersAside

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["filters_aside"] = self.form_class
        request_data = {}
        request_data["method"] = self.request.POST.get('sort_by')
        request_data["category"] = self.request.POST.getlist('category', [])
        request_data["brand"] = self.request.POST.getlist('brand', [])

        service_context = self.service.get_context_data(request_data)
        
        service_context["search_bar"] = SearchForm(categories=service_context["search_bar"])
        return {**context, **service_context}
    
    def get_queryset(self):
        if self.request.method == "POST":
            return self._handle_post_request()
        return self._handle_get_request()

    def _handle_post_request(self):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            self.service.clear_session_data()
            return self.service.filter_products(form.cleaned_data)
        return self.service.get_top_selling()

    def _handle_get_request(self):
        session_data = self.service.get_session_data()
        if self.request.GET.get("clear_session", "false").lower() == "true":
            return self.service.handle_get_request(**self.kwargs)
        if session_data["query"] or session_data["category_id"] != '0':
            return self.service.handle_session_data(session_data)
        return self.service.handle_get_request(**self.kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        self.service.post()
        
        return self.render_to_response(context)
    
    def dispatch(self, request, *args, **kwargs):
        inject_session_dependencies(self, request)
        return super().dispatch(request, *args, **kwargs)

class ProductPage(DetailView, BaseViewMixin):
    model = Product
    service_class = ProductPageService
    service_factory = SERVICE_FACTORY
    repository_classes = {
        "product_rating_repository": DjangoProductRatingRepository,
        "review_repository": DjangoReviewRepository,
        "review_read_model": DjangoReviewReadModel,
    }
    template_name = 'shop/product.html'
    slug_field = "slug" 
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(ProductPage, self).get_context_data(**kwargs)

        service_context = self.service.get_context_data()
    
        service_context["search_bar"] = SearchForm(categories=service_context["search_bar"])
        return {**context, **service_context}
    
    def get_object(self, queryset=None) -> ProductDTO:
        if queryset is None:
            queryset = self.get_queryset()

        return self.service.get_object(self.kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.get_context_data(object=self.object)

        data = request.POST.copy()
        data['product'] = self.object.pk
        data['cart'] = request.user.cart.pk
        form = AddToCartForm(data, object=self.object, cart_pk=request.user.cart.pk)
        if form.is_valid():
            self.service.post()

        return HttpResponseRedirect(self.object.get_absolute_url())
    
    def dispatch(self, request, *args, **kwargs):
        inject_session_dependencies(self, request)
        return super().dispatch(request, *args, **kwargs)


def search(request):
    query = request.GET.get('query', '')
    category_public_uuid = request.GET.get('category', '')

    store_search(query, category_public_uuid, RedisSessionAdapter(RedisAdapter()))

    return HttpResponseRedirect(reverse_lazy('store'))