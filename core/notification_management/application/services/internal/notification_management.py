from django.http import HttpRequest, JsonResponse

from ..external.notification_management import *
from core.notification_management.presentation.notification_management.models import CommonMailingList

import json
import requests

def newsletter_service(request: HttpRequest):
    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    if request.user.is_anonymous:
        return JsonResponse({"status": "error", "message": "Log in for a subscribe to email notification"}, status=401)
    if not "email" in data:
        return JsonResponse({"status": "error", "message": "Insert an email"}, status=400)
    if data["email"] != request.user.email:
        return JsonResponse({"status": "error", "message": f"Incorrect email address: {data["email"]}"}, status=400)
    else:
        try:
            status_code, respond_data = subscribe_user_to_mailchimp(email=data["email"], first_name=data["Fname"], last_name=data["Lname"])
        except requests.exceptions.Timeout:
            return JsonResponse({"status": "error", "message": "timed out"}, status=504)

        if status_code == 200:
            CommonMailingList.objects.create(email=data["email"], user=request.user)
    
    return JsonResponse(respond_data, status=status_code)