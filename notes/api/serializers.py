from rest_framework import serializers
from ..models import Note, NoteAccess
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "visibility"]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long"
            )

        return value

    def validate(self, data):  # type: ignore
        if data["title"] == data["content"]:
            raise serializers.ValidationError("Title must be distinct from content")

        return data

class NoteListSerializer(ModelSerializer):
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ["id", "title", "preview", "visibility", "created_at"]

    def get_preview(self, obj):
        return obj.content[:100]

class ShareItemSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = "user"
    )
    access_level = serializers.ChoiceField(
        choices = NoteAccess.AccessLevel.choices,
        default ="view"
    )

class ShareNoteSerializer(serializers.Serializer):
    shares = ShareItemSerializer(many=True)