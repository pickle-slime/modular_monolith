from django.urls import path
from .views import create_review, load_reviews

urlpatterns = [
    path('home/all-categories/<slug:category>/<slug:product>/reviews/', create_review, name='review'),
    path('home/all-categories/<slug:category>/<slug:product>/load_reviews/', load_reviews, name='load_review'),
]
