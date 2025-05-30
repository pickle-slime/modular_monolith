from core.cart_management.application.dtos.requests import AddWishlistItemRequestDTO, AddCartItemRequestDTO, DeleteWishlistItemRequestDTO, DeleteCartItemRequestDTO
from .view_helper import initiate_cart_service, initiate_wishlist_service

from django.http import JsonResponse

from pydantic import ValidationError
import json


def delete_button_cart(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"message": f"JSON decode error"}, status=400)

        try:
            request_dto = DeleteCartItemRequestDTO(**data)
        except ValidationError:
            return JsonResponse({"message": f"Validation error"}, status=400)

        service = initiate_cart_service(request)
        response, status = service.delete_button_cart_service(request_dto)
        return JsonResponse(response, status=status)

    return JsonResponse({"message": "Invalid data"}, status=400)

def delete_button_wishlist(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"message": f"JSON decode error"}, status=400)

        try:
            request_dto = DeleteWishlistItemRequestDTO(**data)
        except ValidationError:
            return JsonResponse({"message": f"Validation error"}, status=400)

        service = initiate_wishlist_service(request)
        response, status = service.delete_button_wishlist_service(request_dto)
        return JsonResponse(response, status=status)

    return JsonResponse({"message": "Invalid data"}, status=400)

def add_to_wishlist(request):
    if request.method == 'PUT' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"message": f"JSON decode error"}, status=400)

        try:
            validated_dto = AddWishlistItemRequestDTO(**data)
        except ValidationError:
            return JsonResponse({"message": f"Validation error"}, status=400)

        service = initiate_wishlist_service(request)
        response, status = service.add_to_wishlist(validated_dto)
        return JsonResponse(response, status=status)

    return JsonResponse({"message": "Invalid data"}, status=400)

def add_to_cart(request):
    if request.method == 'PUT' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"message": f"JSON decode error"}, status=400)

        try:
            validated_dto = AddCartItemRequestDTO(**data)
        except ValidationError:
            return JsonResponse({"message": f"Validation error"}, status=400)

        service = initiate_cart_service(request)
        response, status = service.add_to_cart(validated_dto)
        return JsonResponse(response, status=status)

    return JsonResponse({"message": "Invalid data"}, status=400)
