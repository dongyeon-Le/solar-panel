from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password  # 비밀번호 검증 함수
from django.core.exceptions import ObjectDoesNotExist

UserModel = get_user_model()

class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(UserId=username)
            # 비밀번호 해시 비교
            if check_password(password, user.UserPassword):  # Django의 비밀번호 체크 함수 사용
                return user
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
