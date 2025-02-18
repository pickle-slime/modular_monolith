from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Custom authentication backend to authenticate using email instead of username.
    """
        
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Treat username as the email
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class JWTAuthenticationBackend(BaseAuthentication):
    """
    Custom authentication class to authenticate a user via JWT.
    """
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return None  # No authorization token

        if len(auth) == 1:
            raise AuthenticationFailed('Authorization token must be bearer token.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Authorization token must be bearer token.')

        token = auth[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = get_user_model().objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token is expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        
        return (user, token)
    
