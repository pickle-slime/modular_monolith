from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomePage.as_view(), name='home'),
    path('home/all-categories/', StorePage.as_view(), name='store'),
    path('home/all-categories/<slug:category>/', StorePage.as_view(), name='category'),
    path('home/all-categories/<slug:brand>/', StorePage.as_view(), name='brand'),
    path('home/all-categories/<slug:category>/<slug:product>/', ProductPage.as_view(), name='product'),
]
