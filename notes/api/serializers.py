from rest_framework import serializers
from ..models import Note, NoteAccess, Tag, Category
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from .utils import extract_tags
User = get_user_model()


""" class TagSerializer(serializers.Serializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"] """

class NoteSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    class Meta:
        model = Note
        fields = ["id", "title", "content", "tags", "created_at", "visibility"]
        read_only_fields =['tags']

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

    def create(self, validated_data):
        content = validated_data.get("content", "")
        tags = extract_tags(content)

        note = Note.objects.create(**validated_data)

        self._attach_tags(note, tags)
        return note

    def update(self, instance, validated_data):
        content = validated_data.get("content", instance.content)
        tags = extract_tags(content)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.tags.clear()
        self._attach_tags(instance, tags)

        return instance

    def _attach_tags(self, note, tag_names):
        print("TAGS:", tag_names)
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            note.tags.add(tag)

class NoteListSerializer(ModelSerializer):
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ["id", "title", "preview", "visibility", "created_at"]

    def get_preview(self, obj):
        content = obj.content or ""
        preview = content[:100]
        return preview + "..." if len(content) > 100 else preview

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



class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
