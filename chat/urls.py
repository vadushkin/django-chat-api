from rest_framework.routers import DefaultRouter
from django.urls import path, include

from chat.views import MessageView

router = DefaultRouter(trailing_slash=False)

router.register("message", MessageView)

urlpatterns = [
    path("", include(router.urls))
]
