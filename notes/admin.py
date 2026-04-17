from django.contrib import admin
from .models import Note, Category, Tag, NoteAccess


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "owner", "visibility", "created_at")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "owner")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ("id", "name")


@admin.register(NoteAccess)
class NoteAccessAdmin(admin.ModelAdmin):
	list_display = ("note", "user", "access_level")
