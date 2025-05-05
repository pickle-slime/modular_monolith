from django.shortcuts import redirect
from django.http import JsonResponse

from .view_helper import initiate_cart_service, initiate_wishlist_service

import json


def delete_button_cart(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == 'PUT':
        data = json.load(request)
        service = initiate_cart_service(request)
        response, status = service.delete_button_cart_service(data, "Cart")
        JsonResponse(response, status=status)

    return redirect('home')

def delete_button_wishlist(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == 'PUT':
        data = json.load(request)
        service = initiate_wishlist_service(request)
        response, status = service.delete_button_wishlist_service(data, "Wishlist")
        return JsonResponse(response, status=status)

    return redirect('home')

def add_to_wishlist(request):
    if request.method == 'PUT' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body.decode('utf-8'))
        service = initiate_wishlist_service(request)
        response, status = service.add_to_wishlist(data, "Wishlist")
        return JsonResponse(response, status=status)

    return JsonResponse({"status": "error", "message": "Invalid data"})

def add_to_cart(request):
    if request.method == 'PUT' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body.decode('utf-8'))
        service = initiate_cart_service(request)
        response, status = service.add_to_cart(data, "Cart")
        return JsonResponse(response, status=status)

    return JsonResponse({"status": "error", "message": "Invalid data"})
