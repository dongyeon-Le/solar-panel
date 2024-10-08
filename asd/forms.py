from django import forms
from .models import Panel
from .models import SignUp_User
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
# 비밀번호 찾기 --------------
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from asd.models import SignUp_User, Location
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re
from django.core.validators import MinValueValidator


# 2024-09-07 추가 --------------------------------노광우---------------------------------
from django.core.validators import MinValueValidator

class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['capacity', 'location', 'modelNamev', 'manufacturer', 'maintenance', 'quantity', 'size', 'date', 'record', 'cause']
        labels = {
            'capacity': '설치 용량 (Kw)',
            'location': '설치 지역',
            'modelNamev': '모델명',
            'manufacturer': '제조업체',
            'maintenance': '관리업체',
            'quantity': '보유 개수 (개)',
            'size': '크기 (m²)',
            'date': '설치일자 (yyyy-mm-dd)',
            'record': '점검기록 (yyyy-mm-dd)',
            'cause': '고장원인',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'record': forms.DateInput(attrs={'type': 'date'}),
            'capacity': forms.NumberInput(attrs={'placeholder': 'Kw'}),
            'quantity': forms.NumberInput(attrs={'placeholder': '개'}),
            'size': forms.NumberInput(attrs={'placeholder': 'm²'}),
        }
        validators = {
            'capacity': [MinValueValidator(1)],
            'size': [MinValueValidator(1)],
            'quantity': [MinValueValidator(1)],
        }




# 로그인 폼
class LoginForm(forms.Form):
    UserId = forms.CharField(max_length=150, label='아이디')
    UserPassword = forms.CharField(widget=forms.PasswordInput, label='비밀번호')

    def clean(self):
        cleaned_data = super().clean()
        UserId = cleaned_data.get('UserId')
        UserPassword = cleaned_data.get('UserPassword')

        # 비밀번호 검증을 위한 부분은 여기서 필요 없습니다.
        return cleaned_data


# 회원가입
class SignUpForm(forms.ModelForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput, label='비밀번호 확인')

    class Meta:
        model = SignUp_User
        fields = ['UserId', 'UserPassword', 'UserName', 'UserEmail', 'UserPhone', 'UserAddress', 'UserAddress_detail']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('UserPassword')
        confirm_password = cleaned_data.get('confirmPassword')

        if password != confirm_password:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return cleaned_data

# 회원정보 수정
class ModifyUserForm(forms.ModelForm):
    class Meta:
        model = SignUp_User
        fields = ['UserId', 'UserEmail', 'UserPhone', 'UserAddress', 'UserAddress_detail']
        widgets = {
            'UserId': forms.TextInput(attrs={'readonly': True}),
            'UserEmail': forms.EmailInput(attrs={'readonly': True}),
            'UserPhone': forms.TextInput(attrs={'readonly': True}),
            'UserAddress': forms.TextInput(attrs={'readonly': False}),
            'UserAddress_detail': forms.TextInput(attrs={'readonly': False}),
        }
        labels = {
            'UserId': '아이디',
            'UserEmail': '이메일',
            'UserPhone': '전화번호',
            'UserAddress': '주소',
            'UserAddress_detail': '상세주소',
        }
    
    def __init__(self, *args, **kwargs):
        super(ModifyUserForm, self).__init__(*args, **kwargs)
        self.fields['UserId'].disabled = True  # 아이디 수정 불가
        self.fields['UserEmail'].disabled = True  # 이메일 수정 불가
        self.fields['UserPhone'].disabled = True  # 전화번호 수정 불가


# 비밀번호 찾기 -----------------------------------------------------------
User = get_user_model()
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 이메일이 데이터베이스에 존재하는지 확인
        if not User.objects.filter(UserEmail=email).exists():
            raise ValidationError('이 이메일 주소는 등록되지 않았습니다.')
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        email = self.cleaned_data["email"]
        associated_users = User.objects.filter(UserEmail=email)  # 이메일 필드명 수정
        if associated_users.exists():
            for user in associated_users:
                self._send_password_reset_email(user, domain_override, subject_template_name,
                                                email_template_name, use_https, token_generator,
                                                from_email, request, html_email_template_name,
                                                extra_email_context)
        return associated_users

    def _send_password_reset_email(self, user, domain_override, subject_template_name,
                                    email_template_name, use_https, token_generator,
                                    from_email, request, html_email_template_name,
                                    extra_email_context):
        """
        비밀번호 재설정 이메일을 보내는 로직을 구현합니다.
        """
        context = {
            'user': user,
            'email': user.UserEmail,
            'domain': domain_override or request.get_host(),
            'site_name': 'MyWebsite',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
        }
        if extra_email_context:
            context.update(extra_email_context)

        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())

        email_body = render_to_string(email_template_name, context)

        email_message = EmailMessage(subject, email_body, from_email, [user.UserEmail])
        if html_email_template_name:
            html_email_body = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email_body, "text/html")

        email_message.send()

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    from_email = 'webmaster@mywebsite.com'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['email_field_name'] = 'UserEmail'  # 이메일 필드명 변경
        return kwargs
# 2024-09-07 추가 --------------------------------노광우---------------------------------
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location  # 수정: 대문자로 시작하는 모델 이름
        fields = ['address', 'latitude', 'longitude']
        labels = {
            'address': '설치 지역',
            'latitude': '위도',
            'longitude': '경도',
            'user_id': '아이디'
        }
        widgets = {
            'address': forms.TextInput(attrs={'readonly': False}),
            'latitude': forms.TextInput(attrs={'readonly': False}),  # 수정: TextInput 사용
            'longitude': forms.TextInput(attrs={'readonly': False}),  # 수정: TextInput 사용
            'user_id': forms.TextInput(attrs={'readonly': False}),
        }

# 비밀번호 재설정 커스텀 페이지(password_reset_confirm.html)
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        label="새 비밀번호",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '새 비밀번호 입력'}),
        min_length=8,
        help_text="비밀번호는 최소 8자 이상이어야 합니다."
    )
    confirm_password = forms.CharField(
        label="새 비밀번호 (확인)",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '새 비밀번호 확인'}),
        help_text="확인을 위해 이전과 동일한 비밀번호를 입력하세요."
    )

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        
        if len(password) < 8:
            raise ValidationError('비밀번호는 최소 8자 이상이어야 합니다.')
        
        if re.search(r'(password|123456|qwerty|abc123)', password, re.IGNORECASE):
            raise ValidationError('통상적으로 자주 사용되는 비밀번호는 사용할 수 없습니다.')

        if password.isdigit():
            raise ValidationError('숫자로만 이루어진 비밀번호는 사용할 수 없습니다.')

        return password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            self.add_error('confirm_password', '비밀번호가 일치하지 않습니다.')

        return cleaned_data

