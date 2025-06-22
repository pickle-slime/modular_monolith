from django.urls import path
from .views import *

urlpatterns = [
    path('home/register/', RegisterUser.as_view(), name='register'),
    path('home/login/', LoginUser.as_view(), name='login'),
    path('home/logout/', logout_user, name='logout'),
]
