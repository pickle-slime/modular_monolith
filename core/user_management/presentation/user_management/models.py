from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .managers import CustomUserManager
import uuid

class CustomUser(AbstractUser):
    '''
    This is a custom model for users, it uses custom manager placed in managers.py.
    It replace username with email while authentification.
    '''
    inner_uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    public_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
