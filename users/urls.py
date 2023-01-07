from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, RegisterView, RefreshView, UserProfileView

router = DefaultRouter(trailing_slash=False)

router.register('profile', UserProfileView)

urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('refresh', RefreshView.as_view(), name='refresh'),
]
