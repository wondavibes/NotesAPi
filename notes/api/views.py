from rest_framework.viewsets import ModelViewSet
from django.db import models
from rest_framework.decorators import action
from .serializers import NoteSerializer, ShareNoteSerializer
from notes.models import Note, Tag, Category
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import NotePermission
from rest_framework import status, filters, viewsets
from rest_framework.response import Response
from ..services import share_note
from django_filters.rest_framework import DjangoFilterBackend
from .filters import NoteFilter

class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, NotePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NoteFilter 
    search_fields  = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self): #type: ignore
            user = self.request.user

            queryset = Note.objects.all()

            if not user.is_authenticated:
                # Anonymous users see only public notes
                return queryset.filter(visibility="public").prefetch_related('tags')

            # Authenticated users see:
            # - Their own notes (as owner)
            # - Notes shared with them (via NoteAccess)
            return queryset.filter(
                models.Q(owner=user) |
                models.Q(shared_with=user) 
            ).distinct().prefetch_related('tags')
    
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, NotePermission])
    def share(self, request, pk=None):
        note = self.get_object()
        if note.owner != request.user:
            return Response({"detail": "Only the owner can share this note."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ShareNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        share_note(note=note, shares=serializer.validated_data["shares"])
        return Response({"detail": "Note shared successfully."}, status=status.HTTP_200_OK)


# ==================== PUBLIC NOTES VIEWSET ====================
# Separate viewset for public notes with AllowAny permissions
# Usage: Register this in urls.py as router.register(r'public', PublicNoteViewSet)
# This will create /api/public/ endpoints for public notes only
# ================================================================


class PublicNoteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Dedicated read-only ViewSet for public notes.
    Accessible by anyone (anonymous or authenticated).
    """
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NoteFilter
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self): #type: ignore
        """Only public notes + optimize with prefetch"""
        return Note.objects.filter(
            visibility="public"
        ).prefetch_related('tags').order_by('-created_at')


class NoteTag(ModelViewSet):
    ...