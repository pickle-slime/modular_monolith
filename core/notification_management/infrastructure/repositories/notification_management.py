from core.notification_management.domain.interfaces.notification_management import INewsLetterRepository
from core.notification_management.domain.entitites.notification_management import NewsLetter as NewsLetterEntity

from core.notification_management.presentation.notification_management.models import CommonMailingList

from typing import Iterator

class DjangoNewsLetterRepsoitory(INewsLetterRepository):
    def fetch_iterator(self) -> Iterator[NewsLetterEntity]:
        pass

    def save(self, newsletter_entity: NewsLetterEntity) -> bool:
        if not newsletter_entity or not isinstance(newsletter_entity, NewsLetterEntity):
            return False
        
        try:
            CommonMailingList.objects.update_or_create(public_uuid=newsletter_entity.public_uuid, defaults=dict(newsletter_entity))
        except:
            return False
        
        return True