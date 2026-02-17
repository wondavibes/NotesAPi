from django.shortcuts import render, redirect, get_object_or_404
from .models import NoteUser
from rest_framework import generics
from .serializers import NoteUserSerializer
from django.contrib.auth import login, authenticate, logout


class UserListCreateView(generics.ListCreateAPIView):
    queryset = NoteUser.objects.all()
    serializer_class = NoteUserSerializer

