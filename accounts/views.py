from django.shortcuts import render, redirect, get_object_or_404
from .models import NoteUser
from rest_framework import generics
from .serializers import NoteUserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserListCreateView(generics.ListCreateAPIView):
    queryset = NoteUser.objects.all()
    serializer_class = NoteUserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = NoteUser.objects.all()
    serializer_class = RegisterSerializer


class Meview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = NoteUserSerializer(request.user)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer