from rest_framework import generics
from .serializers import NoteSerializer
from notes.models import Note
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["title", "created_at"]
    ordering_fields = ["title", "created_at"]
    ordering = ["created_at"]  # default ordering

    def get_queryset(self):  # type: ignore
        if self.request.user.is_staff:
            return Note.objects.all()

        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):  # type: ignore
        if self.request.user.is_staff:
            return Note.objects.all()

        return Note.objects.filter(owner=self.request.user)
