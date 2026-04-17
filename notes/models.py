from django.conf import settings
from django.db import models
from accounts.models import NoteUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'user')
        ordering = ['name']

    def __str__(self):
        return f"#{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)
        
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
    
    category = models.ForeignKey(
            "Category",
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name="notes",
        )
    tags = models.ManyToManyField(Tag, related_name='notes', blank=True)

    def __str__(self):
        return self.title


class NoteAccess(models.Model):
    class AccessLevel(models.TextChoices):
        VIEW = "view", "View"
        EDIT = "edit", "Edit"

    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="accesses")
    user = models.ForeignKey(NoteUser, on_delete=models.CASCADE, related_name="note_accesses")
    access_level = models.CharField(max_length=10, choices=AccessLevel.choices, default="view")

    class Meta:
        unique_together = ("note", "user")


class Category(models.Model):
        owner = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories"
        )
        name = models.CharField(max_length=100)
        created_at = models.DateTimeField(auto_now_add=True)

        class Meta:
            unique_together = (("owner", "name"),)

        def __str__(self):
            return f"{self.name}"








    