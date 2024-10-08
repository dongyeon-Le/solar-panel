from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

# 사용자 모델 매니저
class SignUp_UserManager(BaseUserManager):
    def create_user(self, UserId, UserPassword, UserEmail, UserName, UserPhone, UserAddress, UserAddress_detail, **extra_fields):
        if not UserId:
            raise ValueError('The UserId field must be set')
        user = self.model(UserId=UserId, UserPassword=UserPassword, UserEmail=UserEmail, UserName=UserName, UserPhone=UserPhone, UserAddress=UserAddress, UserAddress_detail=UserAddress_detail, **extra_fields)
        user.set_password(UserPassword)  # 비밀번호 해싱
        user.save(using=self._db)
        return user

    def create_superuser(self, UserId, UserPassword, UserEmail, UserName, UserPhone, UserAddress, UserAddress_detail, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(UserId, UserPassword, UserEmail, UserName, UserPhone, UserAddress, UserAddress_detail, **extra_fields)

# 사용자 모델
class SignUp_User(AbstractBaseUser):
    UserId = models.CharField(max_length=150, unique=True)
    UserPassword = models.CharField(max_length=150)
    UserName = models.CharField(max_length=100)
    UserEmail = models.EmailField(max_length=200, unique=True)
    UserPhone = models.CharField(max_length=15)
    UserAddress = models.CharField(max_length=250)
    UserAddress_detail = models.CharField(max_length=250)

    USERNAME_FIELD = 'UserId'
    REQUIRED_FIELDS = ['UserEmail', 'UserName', 'UserPhone', 'UserAddress', 'UserAddress_detail']

    objects = SignUp_UserManager()

    def set_password(self, raw_password):
        self.UserPassword = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return self.UserPassword == make_password(raw_password, self.UserPassword)


# 패널 모델
class Panel(models.Model):
    user = models.ForeignKey('SignUp_User', on_delete=models.CASCADE)  # 사용자와 패널 정보를 연결 (사용자가 삭제되면 패널 정보도 삭제됨)
    capacity = models.CharField(max_length=100)  # 설치 용량
    location = models.CharField(max_length=100)  # 설치 지역
    modelNamev = models.CharField(max_length=100, null=True, blank=True)  # 모델명 (선택 사항)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)  # 제조업체 (선택 사항)
    maintenance = models.CharField(max_length=100, null=True, blank=True)  # 관리 업체 (선택 사항)
    quantity = models.IntegerField()  # 보유 개수
    size = models.FloatField(null=True, blank=True)  # 패널 크기 (선택 사항)
    date = models.DateField(null=True, blank=True)  # 설치 일자 (선택 사항)
    power = models.FloatField()  # 발전량
    record = models.DateField(null=True, blank=True)  # 점검 기록 날짜 (선택 사항)
    cause = models.CharField(max_length=100, null=True, blank=True)  # 고장 원인 (선택 사항)
    state = models.IntegerField()

    def __str__(self):
        return f"{self.modelNamev} - {self.location}"  # 패널의 모델명과 설치 지역을 문자열로 반환


# 위치 경도 모델
class Location(models.Model):
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    user_id = models.FloatField()

    def __str__(self):
        return self.address