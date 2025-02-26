from django.http import HttpRequest
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.cart_management.presentation.acl_factory import CartManagementACLFactory

def inject_session_dependencies_into_view(view_instance, request: HttpRequest) -> None:
    """
    Helper function to inject session-related dependencies dynamically into a view instance that has the BaseViewMixin.
    """
    session_adapter = RedisSessionAdapter(RedisAdapter(), session_key=request.session_key)
    cart_acl = CartManagementACLFactory.create_cart_acl(session_adapter)
    
    view_instance.service_classes["cart_acl"] = cart_acl

    view_instance.adapter_classes["session_adapter"] = session_adapter