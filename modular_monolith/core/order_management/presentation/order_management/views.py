from django.views.generic import FormView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CheckoutForm
from core.order_management.application.services.internal.order_management import CheckoutService

from core.utils.application.base_view_mixin import BaseViewMixin

from typing import Any

class CheckoutPage(BaseViewMixin, LoginRequiredMixin, FormView):
    form_class = CheckoutForm
    service_class = CheckoutService
    template_name = 'order_management/checkout.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return self.service.get_context_data(self.request, context)

    def form_valid(self, form):
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.extra_context = self.service.form_valid(self.request, form)
            return JsonResponse({'status': 'succeed'})
        
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

        return super().form_invalid(form)