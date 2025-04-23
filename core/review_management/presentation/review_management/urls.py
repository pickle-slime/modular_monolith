from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import create_review, load_reviews

urlpatterns = [
    path('home/all-categories/<slug:category>/<slug:product>/reviews/', create_review, name='review'),
    path('home/all-categories/<slug:category>/<slug:product>/load_reviews/', load_reviews, name='load_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
