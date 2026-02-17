from django.conf import settings
from django.db import models
from accounts.models import NoteUser

class Note(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    visibility = models.CharField(
    max_length=20, choices=Visibility.choices, default=Visibility.PRIVATE)
    """shared_with = models.ManyToManyField(
            settings.AUTH_USER_MODEL, related_name="shared_notes", blank=True"""


    def __str__(self):
        return self.title


class NoteAccess(models.Model):
    class AccessLevel(models.TextChoices):
        VIEW = "view", "View"
        EDIT = "edit", "Edit"

    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="accesses")
    user = models.ForeignKey(NoteUser, on_delete=models.CASCADE, related_name="note_accesses")
    access_level = models.CharField(max_length=10, choices=AccessLevel.choices)

    class Meta:
        unique_together = ("note", "user")