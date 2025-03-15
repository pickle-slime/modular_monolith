from django.shortcuts import redirect
from django.http import JsonResponse

from core.review_management.application.services.internal.review_management import *
from core.review_management.infrastructure.repositories.review_management import DjangoProductRatingRepository, DjangoReviewReadModel

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
        product_rating_pub_uuid = request.GET.get("product_rating_uuid", None)
        page_number = request.GET.get('page', None)

        if product_rating_pub_uuid == "" or "null": product_rating_pub_uuid = None
        if page_number == "" or "null": page_number = None

        return JsonResponse(service.load_reviews(product_rating_pub_uuid, page_number))
