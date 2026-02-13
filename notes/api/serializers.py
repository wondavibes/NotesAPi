from rest_framework import serializers
from ..models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "visibility", "shared_with"]

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
