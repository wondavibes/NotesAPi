# notes/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import NoteViewSet, PublicNoteViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'public', PublicNoteViewSet, basename='public')

urlpatterns = [
    path('', include(router.urls)),
]