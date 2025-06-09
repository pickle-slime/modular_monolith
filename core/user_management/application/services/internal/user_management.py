from core.user_management.domain.interfaces.hosts.jwtoken import TokenHost
from core.user_management.domain.entities.user_management import User as UserEntity
from core.user_management.application.dtos.user_management import UserDTO
from core.user_management.domain.events.event_registry import DomainEventRegistry
from core.user_management.application.events.acl_events import NewUserACLEvent
from ..base_service import BaseTemplateService

from core.utils.application.base_service import Service

from typing import Generic, Any
from datetime import datetime

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
    def register_user(self, raw_user_data: dict[str, Any]) -> tuple[UserDTO, str, str]:
        actual_pasword = raw_user_data["password"]
        raw_user_data["password"] = self.password_hasher.hash(raw_user_data["password"]) 

        user_entity = self.create_user_entity(raw_user_data)

        user_entity = self.user_rep.create(user_entity)
        
        refresh_token, access_token = self.authenticate(email=user_entity.email, password=actual_pasword)

        return UserDTO.from_entity(user_entity), refresh_token, access_token

    def create_user_entity(self, user_data: dict[str, Any]) -> UserEntity:
        with DomainEventRegistry.scope():
            entity = UserEntity(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=user_data["password"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    date_joined=datetime.now(),
                    last_login=datetime.now(),
                    role="user",
                )
            events = DomainEventRegistry.pop_events()
            if not events:
                raise RuntimeError("UserEntity did not emit any events")
            if len(events) > 1:
                raise RuntimeError("UserEntity emitted multiple events; only processing the first")

            self.event_bus.publish(NewUserACLEvent.from_domain_event(events[0]))
            return entity
            

class AuthenticationLoginUserService(BaseTemplateService['AuthenticationLoginUserService']):
    pass
