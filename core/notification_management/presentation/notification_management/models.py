from django.db import models

import uuid

class CommonMailingList(models.Model):
    inner_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    public_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(db_index=True)
    user = models.ForeignKey("user_management.CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email} of mailing list"
