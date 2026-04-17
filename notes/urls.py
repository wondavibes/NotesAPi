# notes/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import NoteViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
]