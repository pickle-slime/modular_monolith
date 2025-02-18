"""
URL configuration for electro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.v1.urls')),

    path('', include('core.shop_management.presentation.shop_management.urls')),
    path('', include('core.user_management.presentation.user_management.urls')),
    path('', include('core.cart_management.presentation.cart_management.urls')),
    path('', include('core.order_management.presentation.order_management.urls')),
    path('', include('core.review_management.presentation.review_management.urls')),
    path('', include('core.payment_management.presentation.payment_management.urls')),
    path('', include('core.notification_management.presentation.notification_management.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

