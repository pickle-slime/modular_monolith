from core.user_management.domain.interfaces.i_repositories.i_user_management import IUserRepository
from core.user_management.domain.entities.user_management import User as UserEntity
from core.user_management.presentation.user_management.models import CustomUser as UserModel

from ..mappers.user_management import DjangoUserMapper

from core.exceptions import UserAlreadyExistsError
import uuid

class DjangoUserRepository(IUserRepository):    
    def find_by_email(self, email: str) -> UserEntity:
        try:
            return DjangoUserMapper.map_user_into_entity(UserModel.objects.get(email=email)) 
        except UserModel.DoesNotExist:
            return UserEntity.guest()
        
    def find_by_uuid(self, inner_uuid: uuid.UUID | None = None, public_uuid: uuid.UUID | None = None) -> UserEntity:
        try:
            entity = UserEntity()
            if inner_uuid:
                entity = DjangoUserMapper.map_user_into_entity(UserModel.objects.get(inner_uuid=inner_uuid)) 
            elif public_uuid:
                entity = DjangoUserMapper.map_user_into_entity(UserModel.objects.get(public_uuid=public_uuid)) 
            return entity
        except UserModel.DoesNotExist:
            return UserEntity.guest()

    def save(self, user: UserEntity) -> tuple[UserEntity, bool]:
        model, created = UserModel.objects.update_or_create(
            public_uuid=user.public_uuid,
            defaults={
                'inner_uuid': user.inner_uuid,
                'public_uuid': user.public_uuid,
                'username': user.username,
                'password': user.hashed_password,
                'fisrt_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
            }
        )
        return DjangoUserMapper.map_user_into_entity(model), created

    def create(self, user: UserEntity) -> UserEntity:
        existing = UserModel.objects.filter(public_uuid=user.public_uuid).first()
        if existing:
            raise UserAlreadyExistsError("User with this UUID already exists.")
        
        model = UserModel.objects.create(
            public_uuid=user.public_uuid,
            inner_uuid=user.inner_uuid,
            username=user.username,
            password=user.hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            date_joined=user.date_joined,
            last_login=user.last_login,
        )

        return DjangoUserMapper.map_user_into_entity(model)
