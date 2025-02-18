"""
WSGI config for electro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os, sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.presentation.electro.settings')  

#project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(project_root)

# Add your custom path to PYTHONPATH
sys.path.append(os.path.join(BASE_DIR, 'core', 'presentation'))

# Add each bounded context's 'presentation' directory to sys.path
bounded_contexts = os.getenv("BOUNDED_CONTEXTS", 'shop_management,user_management,cart_management,review_management,notification_management,order_management,payment_management').split(",")
for context in bounded_contexts:
    presentation_path = os.path.join(BASE_DIR, 'core', context, 'presentation')
    sys.path.append(presentation_path)

application = get_wsgi_application()
