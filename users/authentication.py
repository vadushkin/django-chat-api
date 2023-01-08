from datetime import datetime

import jwt
from django.conf import settings
from jwt import DecodeError
from rest_framework.authentication import BaseAuthentication

from .models import CustomUser


class Authentication(BaseAuthentication):
    def authenticate(self, request):
        data = self.validate_request(request.headers)

        if not data:
            return None, None

        return self.get_user(data["user_id"]), None

    @staticmethod
    def get_user(user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

        return user

    @staticmethod
    def validate_request(headers):
        authorization = headers.get("Authorization", None)

        if not authorization:
            return None

        token = headers["Authorization"][7:]
        decoded_data = Authentication.verify_token(token)

        if not decoded_data:
            return None

        return decoded_data

    @staticmethod
    def verify_token(token):
        try:
            decoded_data = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms="HS256"
            )
        except DecodeError:
            return None

        exp = decoded_data["exp"]

        if datetime.now().timestamp() > exp:
            return None

        return decoded_data
