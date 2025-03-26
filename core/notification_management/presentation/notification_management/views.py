from django.http import JsonResponse
from django.views import View

from core.notification_management.application.services.internal.notification_management import NewsLetterService

from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.user_management.presentation.acl_factory import UserManagementACLFactory

import json

class NewsLetterView(View):
    service = NewsLetterService(RedisSessionAdapter(RedisAdapter()), UserManagementACLFactory.create_user_acl())

    def resolve_session_key(self, session_key: str):
        self.service.session.hand_over_session_key(session_key)

    def dispatch(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax and request.method == 'POST':

            self.resolve_session_key(request.session_key)
            
            try:
                data = json.loads(request.body)
            except json.decoder.JSONDecodeError:
                return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)
            
            response, status = self.service.newsletter_service(data)
            return JsonResponse(response, status=status)

        return JsonResponse({"status": "error", "message": "Something went wrong"}, status=400)
