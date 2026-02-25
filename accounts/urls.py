from django.urls import path
from .views import (
    UserListCreateView,
    RegisterView,
    Meview,
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', Meview.as_view(), name='me'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
