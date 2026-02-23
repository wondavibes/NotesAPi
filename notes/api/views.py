from rest_framework.viewsets import ModelViewSet
from django.db import models
from rest_framework.decorators import action
from .serializers import NoteSerializer, ShareNoteSerializer
from notes.models import Note
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import NotePermission
from rest_framework import status
from rest_framework.response import Response
from ..services import share_note



class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, NotePermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self): # type: ignore
        user = self.request.user

        if not user.is_authenticated:
            return Note.objects.filter(visibility="public")
        
        return Note.objects.filter(
            models.Q(owner=user) |
            models.Q(shared_with=user)
        ).distinct()
    
    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def public(self, request):
        public_notes = Note.objects.filter(visibility="public")
        serializer = self.get_serializer(public_notes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, NotePermission])
    def share(self, request, pk=None):
        note = self.get_object()
        if note.owner != request.user:
            return Response({"detail": "Only the owner can share this note."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ShareNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        share_note(note=note, shares=serializer.validated_data["shares"])
        return Response({"detail": "Note shared successfully."}, status=status.HTTP_200_OK)