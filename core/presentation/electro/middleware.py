# myapp/middleware.py
from core.user_management.infrastructure.adapters.jwtoken import JWTokenAdapter
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.user_management.application.services.internal.user_management import AuthenticationUserMiddlewareService
from config import JWT_SECRET_KEY, ACCESS_JWTOKEN_EXPIRY, REFRESH_JWTOKEN_EXPIRY
from django.utils.deprecation import MiddlewareMixin

from core.user_management.presentation.user_management.views import logout_user

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.token_service = AuthenticationUserMiddlewareService(
            JWTokenAdapter(
                secret_key=JWT_SECRET_KEY,
                access_token_expiry=ACCESS_JWTOKEN_EXPIRY,
                refresh_token_expiry=REFRESH_JWTOKEN_EXPIRY
            )
        )

    def __call__(self, request):
        self._process_request(request)
        response = self.get_response(request)
        self._add_authorization_headers(response, request)
        
        return response

    def _process_request(self, request):
        """
        Validates the access token and refresh token from cookies.
        """
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")
        request.jwt = {"authorized": False, "error": None, "new_access_token": None, "decoded_token": None}

        if access_token:
            try:
                if self.token_service.is_token_expired(access_token):
                    raise ValueError("Access token expired.")
                
                decoded_token = self.token_service.decode_token(access_token)
                request.jwt.update({"authorized": True, "decoded_token": decoded_token})
            except (IndexError, ValueError) as e:
                request.jwt["error"] = str(e)

        elif refresh_token:
            try:
                new_access_token = self.token_service.refresh_access_token(refresh_token)
                if not new_access_token:
                    raise ValueError("Invalid refresh token")
                decoded_token = self.token_service.decode_token(new_access_token)
                request.jwt.update({
                    "authorized": True,
                    "decoded_token": decoded_token,
                    "new_access_token": new_access_token,
                })
            except Exception as e:
                request.jwt["error"] = str(e)

        else:
            request.jwt["error"] = "Authorization header or refresh token is missing."

    def _add_authorization_headers(self, response, request):
        """
        Adds necessary headers or cookies to the response based on authorization.
        """
        jwt_info = getattr(request, "jwt", {})
        authorized = jwt_info.get("authorized", False)
        error = jwt_info.get("error")
        new_access_token = jwt_info.get("new_access_token")

        response["Authorized"] = "true" if authorized else "false"
        if error:
            response["Auth-Error"] = error

            if error == "Access token expired":
                response.delete_cookie("access_token")
            elif error == "Expired refresh token":
                logout_user(request)

        if new_access_token:
            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=True,
                samesite="Strict"
            )



class SessionPopulatedMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.session_adapter = RedisSessionAdapter(RedisAdapter())

    def __call__(self, request):
        self._process_request(request)
        response = self.get_response(request)
        self._handle_response(request, response)

        return response

    def _process_request(self, request):   
        session_key = request.COOKIES.get("session_key")
        
        if not session_key:
            request.session_key = self.session_adapter.session_key
        else:
            self.session_adapter.hand_over_session_key(session_key)
            request.session_key = session_key

        self.session_adapter.set(key="path", data=request.path)

        if hasattr(request, 'jwt'):
            is_authorized = request.jwt.get('authorized', False)
            self.session_adapter.set(key='is_authorized', data=is_authorized)

            if not request.jwt['decoded_token'] is None:
                user_public_uuid = request.jwt['decoded_token'].get('user_public_uuid', None)
            else:
                return None

            if is_authorized and user_public_uuid:
                self.session_adapter.set(key='user_public_uuid', data=user_public_uuid)

    def _handle_response(self, request, response):
        response.set_cookie(
            key="session_key",
            value=request.session_key,
            httponly=True,
            secure=True,
            samesite="Strict"
        )
