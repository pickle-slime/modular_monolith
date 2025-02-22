from core.user_management.domain.interfaces.hosts.jwtoken import TokenHost
from ..base_service import BaseTemplateService

from core.utils.application.base_service import Service

from typing import Generic

class AuthenticationUserMiddlewareService(Generic[Service]):
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
    
    
class AuthenticationRegisterUserService(BaseTemplateService['AuthenticationRegisterUserService']):
    pass

class AuthenticationLoginUserService(BaseTemplateService['AuthenticationLoginUserService']):
    pass