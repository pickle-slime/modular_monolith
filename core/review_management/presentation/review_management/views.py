from django.shortcuts import redirect
from django.http import JsonResponse

from core.review_management.application.services.internal.review_management import *
from core.review_management.infrastructure.repositories.review_management import DjangoProductRatingRepository, DjangoReviewReadModel
from core.review_management.presentation.review_management.forms import ReviewForm

import json

def create_review(request, category, product):
    service = ProductPageReviewsService(DjangoProductRatingRepository(), DjangoReviewReadModel())
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        data = json.load(request)
        form = ReviewForm(data)
        if form.is_valid():
            return JsonResponse(service.create_review(form.cleaned_data))
    return redirect('home')

def load_reviews(request, category, product):
    service = ProductPageReviewsService(DjangoProductRatingRepository(), DjangoReviewReadModel())
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET':
        product_rating_pub_uuid: uuid.UUID | None = request.GET.get("product_rating_uuid", None)
        page_number: int = request.GET.get('page', 1)

        if product_rating_pub_uuid == "" or product_rating_pub_uuid == "null": product_rating_pub_uuid = None
        if page_number == "" or page_number == "null": page_number = 1

        return JsonResponse(service.load_reviews(product_rating_pub_uuid, page_number))
