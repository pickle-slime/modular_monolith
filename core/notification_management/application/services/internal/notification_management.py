from ..external.notification_management import MailchipService
from core.notification_management.application.dtos.acl_dtos import ACLUserDTO

from core.notification_management.presentation.notification_management.models import CommonMailingList

from core.utils.domain.interfaces.hosts.redis import RedisSessionHost
from core.user_management.domain.interfaces.i_acls import IUserACL

from typing import Any
import requests

class NewsLetterService:
    mailchimp = MailchipService()

    def __init__(self, session_adapter: RedisSessionHost, user_acl: IUserACL, newsletter_repository = None):
        self.session = session_adapter
        self.user_acl = user_acl
        self.newsletter_rep = newsletter_repository

    @property
    def user(self) -> ACLUserDTO:
        if not hasattr(self, "_user"):
            user_public_uuid = self.session.get('user_public_uuid', None)
            user = self.user_acl.fetch_by_uuid(public_uuid=user_public_uuid) if user_public_uuid else self.user_acl.guest()
            self._user = ACLUserDTO.from_user_dto(user)
        return self._user
    
    @property
    def is_authorized(self) -> bool:
        if not hasattr(self, "_is_authorized"):
            self._is_authorized = self.session.get('is_authorized', False)
        return self._is_authorized

    def newsletter_service(self, data: dict[str, Any]) -> tuple[dict, int]:
        if not self.is_authorized:
            return {"status": "error", "message": "Log in for a subscribe to email notification"}, 401
        elif not "email" in data:
            return {"status": "error", "message": "Insert an email"}, 400
        elif data["email"] != self.user.email:
            return {"status": "error", "message": f"Incorrect email address: {data["email"]}"}, 400
        else:
            try:
                status_code, respond_data = self.mailchimp.subscribe_user_to_mailchimp(email=data["email"], first_name=data["Fname"], last_name=data["Lname"])
            except requests.exceptions.Timeout:
                return {"status": "error", "message": "timed out"}, 504

            if status_code == 200:
                CommonMailingList.objects.create(email=data["email"], user=request.user)
        
        return respond_data, status_code
