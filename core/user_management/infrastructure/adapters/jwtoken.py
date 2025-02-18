from core.user_management.domain.interfaces.hosts.jwtoken import TokenHost

from datetime import datetime, timedelta, timezone
import uuid
import jwt

class JWTokenAdapter(TokenHost):
    def __init__(self, secret_key: str, access_token_expiry: int, refresh_token_expiry: int):
        self.secret_key = secret_key
        self.access_token_expiry = access_token_expiry
        self.refresh_token_expiry = refresh_token_expiry
    
    def generate_access_token(self, user_public_uuid: uuid.UUID):
        return self._generate_token(user_public_uuid, self.access_token_expiry)
    
    def refresh_token(self, user_public_uuid: uuid.UUID):
        return self._generate_token(user_public_uuid, self.refresh_token_expiry)
    
    def _generate_token(self, user_public_uuid: uuid.UUID, expiry_minutes: int):
        payload = {
            "user_public_uuid": str(user_public_uuid),
            "exp": datetime.now() + timedelta(minutes=expiry_minutes),
            "iat": datetime.now()
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def decode_token(self, token):
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def is_token_expired(self, token) -> bool:
        decoded_token = self.decode_token(token)
        if decoded_token:
            exp_timestamp = decoded_token.get('exp')
            if exp_timestamp and datetime.fromtimestamp(exp_timestamp, timezone.utc) > datetime.now(timezone.utc):
                return False
        return True