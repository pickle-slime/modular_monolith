from django.db import models

import uuid

class CommonMailingList(models.Model):
    inner_uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    public_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey("user_management.CustomUser", on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.public_uuid} - Subscribed on {self.subscribed_at}" 