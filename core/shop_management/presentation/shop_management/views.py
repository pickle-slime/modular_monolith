from typing import Any

from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect

from core.utils.presentation.session_helper import inject_session_dependencies_into_view

from .forms import *
from .models import Product
from core.shop_management.application.services.internal.shop_management import *

from core.utils.application.base_view_mixin import BaseViewMixin
from core.utils.application.base_factories import BaseServiceFactory
from core.shop_management.infrastructure.repositories.shop_management import DjangoProductRepository, DjangoCategoryRepository, DjangoBrandRepository
from core.cart_management.presentation.cart_management.forms import AddToCartForm, AddToWishlistForm
from core.cart_management.presentation.acl_factory import CartManagementACLFactory
from core.user_management.presentation.acl_factory import UserManagementACLFactory
from core.review_management.presentation.acl_factory import ReivewManagementACLFactory
from core.utils.infrastructure.adapters.dj_url_mapping import DjangoURLAdapter

SERVICE_FACTORY = BaseServiceFactory(
    services={
        "cart_acl": None, #requires session adapter
        "wishlist_acl": CartManagementACLFactory.create_wishlist_acl(),
        "user_acl": UserManagementACLFactory.create_user_acl(),
    },
    repositories={
        "category_repository": DjangoCategoryRepository,
        "product_repository": DjangoProductRepository,
        "brand_repository": DjangoBrandRepository,
    },
    adapters={
        "url_mapping_adapter": DjangoURLAdapter,
        "session_adapter": None #requires session_key which is restored in request.session_key
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
        inject_session_dependencies_into_view(self, request)
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
            return self.service.filter_products(form.cleaned_data)
        return self.service.get_top_selling()

    def _handle_get_request(self):
        navigation = True if self.request.GET.get("navigation", "false").lower() == "true" else False
        category = self.request.GET.get("category", None)
        query = self.request.GET.get("query", None)
        return self.service.handle_get_request(category, query, navigation, self.kwargs.get("category", None))
   
    def post(self):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        self.service.post()
        
        return self.render_to_response(context)
    
    def dispatch(self, request, *args, **kwargs):
        inject_session_dependencies_into_view(self, request)
        return super().dispatch(request, *args, **kwargs)

class ProductPage(DetailView, BaseViewMixin):
    model = Product
    service_class = ProductPageService
    service_factory = SERVICE_FACTORY
    repository_classes = {
        "product_rating_acl": ReivewManagementACLFactory.create_product_rating_acl(),
    }
    template_name = 'shop/product.html'
    slug_field = "slug" 
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(ProductPage, self).get_context_data(**kwargs)

        service_context = self.service.get_context_data()

        service_context["search_bar"] = SearchForm(categories=service_context["search_bar"])
        if self.service.user.is_authenticated:
            object_entity, cart_uuid, wishlist_uuid = service_context["add_to_cart_and_wishlist"]
            service_context["add_to_cart"] = AddToCartForm(object_dto=object_entity, cart_uuid=cart_uuid)
            service_context["add_to_wishlist"] = AddToWishlistForm(object_dto=object_entity, wishlist_uuid=wishlist_uuid)

        return {**context, **service_context}
    
    def get_object(self, queryset=None) -> ProductDTO:
        if queryset is None:
            queryset = self.get_queryset()

        return self.service.get_object(self.kwargs)

    def post(self, request):
        self.object = self.get_object()
        self.get_context_data(object=self.object)

        data = request.POST.copy()
        form = AddToCartForm(data, object_entity=self.object, cart_uuid=self.request.user.cart.public_uuid
)
        if form.is_valid():
            self.service.post()

        return HttpResponseRedirect(self.object.get_absolute_url())
    
    def dispatch(self, request, *args, **kwargs):
        inject_session_dependencies_into_view(self, request)
        return super().dispatch(request, *args, **kwargs)

