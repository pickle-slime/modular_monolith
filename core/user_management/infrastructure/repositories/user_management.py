from core.user_management.domain.interfaces.i_repositories.i_user_management import IUserRepository
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost
from core.user_management.domain.entities.user_management import User as UserEntity

from core.user_management.presentation.user_management.models import CustomUser as UserModel

import uuid

class DjangoUserRepository(IUserRepository):
    @staticmethod
    def map_user_into_entity(model: UserModel) -> UserEntity:
        return UserEntity(
            inner_uuid=model.inner_uuid,
            public_uuid=model.public_uuid,
            username=model.username,
            email=model.email,
            hashed_password=model.password,
            first_name=model.first_name,
            last_name=model.last_name,
            date_joined=model.date_joined,
            last_login=model.last_login,
        )
    
    def find_by_email(self, email: str) -> UserEntity:
        try:
            return self.map_user_into_entity(UserModel.objects.get(email=email)) 
        except UserModel.DoesNotExist:
            return UserEntity(inner_uuid=None, public_uuid=None)
        
    def find_by_uuid(self, inner_uuid: uuid.UUID = None, public_uuid: uuid.UUID = None) -> UserEntity:
        try:
            entity = UserEntity(inner_uuid=None, public_uuid=None)
            if inner_uuid:
                entity = self.map_user_into_entity(UserModel.objects.get(inner_uuid=inner_uuid)) 
            elif public_uuid:
                entity = self.map_user_into_entity(UserModel.objects.get(public_uuid=public_uuid)) 
            return entity
        except UserModel.DoesNotExist:
            return UserEntity(inner_uuid=None, public_uuid=None)

    def save(self, user: UserEntity) -> bool:
        model, created = UserModel.objects.update_or_create(
            public_uuid=user.public_uuid,
            defaults={
                'inner_uuid': user.inner_uuid,
                'public_uuid': user.public_uuid,
                'username': user.username,
                'password': user.hashed_password,
                'email': user.email,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'is_authenticated': user.is_authenticated,
                'role': user.role,
            }
        )
        return self.map_user_into_entity(model), created