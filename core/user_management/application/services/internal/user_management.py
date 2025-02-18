from typing import Any

from core.utils.application.base_service import TemplateService
from core.user_management.domain.interfaces.hosts.jwtoken import TokenHost
from core.user_management.domain.interfaces.hosts.password_hasher import PasswordHasherHost

class AuthenticationUserMiddlewareService:
    def __init__(self, token_adapter: TokenHost):
        self.token_adapter = token_adapter

    def refresh_access_token(self, refresh_token):
        if self.token_adapter.is_token_expired(refresh_token):
            raise ValueError("Expired refresh token")
        
        decoded_refresh_token = self.token_adapter.decode_token(refresh_token)
        
        return self.token_adapter.generate_access_token(decoded_refresh_token["user_public_uuid"])
    
    def decode_token(self, token):
        return self.token_adapter.decode_token(token)
    
    def is_token_expired(self, token):
        return self.token_adapter.is_token_expired(token)

class AuthenticationUserService:
    def __init__(self, token_adapter: TokenHost, template_service: TemplateService):
        self.template_service = template_service
        self.token_adapter = token_adapter

    def authenticate(self, email, password, password_hasher: PasswordHasherHost) -> tuple[str, str]:
        ''' Returns refresh token and access token accordingly '''
        user = self.template_service.user_rep.find_by_email(email)
        if not user or not user.check_password(password, password_hasher):
            raise ValueError("Invalid credentials")
        refresh_token = self.token_adapter.refresh_token(user.public_uuid)
        access_token = self.token_adapter.generate_access_token(user.public_uuid)
        return refresh_token, access_token
    
    def get_context_data(self, context: dict[str: Any]) -> dict[str: Any]:
        return {**self.template_service.get_header_and_footer(), **context}
    
class AuthenticationRegisterUserService(AuthenticationUserService):
    pass

class AuthenticationLoginUserService(AuthenticationUserService):
    pass