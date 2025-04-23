from core.user_management.domain.entities.user_management import User as UserEntity
from core.user_management.domain.value_objects.user_management import RoleField
from core.user_management.presentation.user_management.models import CustomUser as UserModel

class DjangoUserMapper:
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
            role=RoleField(DjangoUserMapper.resolve_django_roles(model))
        )

    @staticmethod
    def resolve_django_roles(model: UserModel) -> str:
        if model.is_superuser == True: return 'admin'
        if model.is_staff == True: return 'manager'
        return 'customer'
