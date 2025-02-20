from django.http import HttpRequest
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.cart_management.presentation.acl_factory import CartManagementACLFactory

def inject_session_dependencies(view_instance, request: HttpRequest) -> None:
    """
    Helper function to inject session-related dependencies dynamically into a view instance.
    """
    session_adapter = RedisSessionAdapter(RedisAdapter(), session_key=request.session.session_key)
    cart_acl = CartManagementACLFactory.create_cart_acl(session_adapter)
    
    view_instance.service_factory._services["cart_acl"] = cart_acl

    view_instance.service_factory._adapters["session_adapter"] = session_adapter
