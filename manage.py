#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.presentation.electro.settings')

    # Add your custom path to PYTHONPATH
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core', 'presentation'))

    # Add each bounded context's 'presentation' directory to sys.path
    bounded_contexts = os.getenv("BOUNDED_CONTEXTS", 'shop_management,user_management,cart_management,review_management,notification_management,order_management,payment_management').split(",")
    for context in bounded_contexts:
        presentation_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core', context, 'presentation')
        sys.path.append(presentation_path)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if "--debugpy" in sys.argv:
        import debugpy
        debugpy.listen(("127.0.0.1", 5678))
        print("waiting for debuger to attach")
        debugpy.wait_for_client()
        sys.argv.remove("--debugpy")
    main()
