from core.notification_management.domain.entities.notification_management import NewsLetter as NewsLetterEntity
from core.notification_management.presentation.notification_management.models import CommonMailingList
from core.utils.domain.value_objects.common import CommonEmailField


class NewsLetterMapper:
    @staticmethod
    def map_into_entity(model: CommonMailingList) -> NewsLetterEntity:
        return NewsLetterEntity(
                inner_uuid=model.inner_uuid,
                public_uuid=model.public_uuid,
                email=CommonEmailField(model.email),
                subscribed_at=model.subscribed_at,
                user=model.user.public_uuid,
        )
