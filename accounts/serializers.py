from rest_framework import serializers
from .models import NoteUser

class NoteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteUser
        fields = ['id', 'username', 'email', 'is_staff', 'is_active']
        