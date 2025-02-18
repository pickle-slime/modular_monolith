from django.http import HttpRequest
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter, RedisAdapter
from core.cart_management.infrastructure.repositories.cart_management import DjangoCartRepository
from core.cart_management.presentation.acl_factory import CartManagementACLFactory

def inject_session_dependencies(view_instance, request: HttpRequest) -> None:
    """
    Helper function to inject session-related dependencies dynamically into a view instance.
    """
    session_adapter = RedisSessionAdapter(RedisAdapter(), session_key=request.session.session_key)
    cart_acl = CartManagementACLFactory.create_cart_acl(session_adapter) #DjangoCartRepository(session_adapter=session_adapter)
    
    # Inject the session adapter into relevant parts (e.g., repositories or services)
    view_instance.setup_dynamic_dependencies(
        instance_name="template_service",
        dependencies={"cart_acl": cart_acl}
    )
    
    view_instance.setup_dynamic_dependencies(
        instance_name="template_service",
        dependencies={"session_adapter": session_adapter}
    )
