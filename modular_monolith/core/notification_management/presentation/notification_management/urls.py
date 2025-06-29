from django.urls import path
from .views import NewsLetterView

urlpatterns = [
    path('api/ajax-newsletter/', NewsLetterView.as_view(), name='newsletter'),
]
