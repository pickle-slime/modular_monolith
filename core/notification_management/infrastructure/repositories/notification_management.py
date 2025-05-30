from core.notification_management.domain.interfaces.notification_management import INewsLetterRepository
from core.notification_management.domain.entities.notification_management import NewsLetter as NewsLetterEntity
from ..mappers.notification_management import NewsLetterMapper

from core.notification_management.presentation.notification_management.models import CommonMailingList

from typing import Iterator
import uuid

class DjangoNewsLetterRepsoitory(INewsLetterRepository):
    def fetch_iterator(self) -> Iterator[NewsLetterEntity]:
        ...

    def create(self, email: str, user_public_uuid: uuid.UUID | None = None) -> NewsLetterEntity | None:
        if not email:
            return None
        
        try:
            model = CommonMailingList.objects.create(email=email, user_public_uuid=user_public_uuid)
            entity = NewsLetterMapper.map_into_entity(model)
        except:
            return None
        
        return entity
