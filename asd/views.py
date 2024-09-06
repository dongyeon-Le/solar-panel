from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import SignUp_User  # 모델 이름 변경
from .forms import SignUpForm, LoginForm, PanelForm

#---------------------------------------------------------------

## 메인페이지
def main_view(request):
    form = LoginForm()
    return render(request, 'asd/main/basic/main.html', {'form': form})

## 메인페이지 - 상단 (목록)
def main_list_1_view(request):
    return render(request, 'asd/main/list/main_list_1.html')  # 메인 목록1
def main_list_2_view(request):
    return render(request, 'asd/main/list/main_list_2.html')  # 메인 목록2
def main_list_3_view(request):
    return render(request, 'asd/main/list/main_list_3.html')  # 메인 목록3
def main_list_4_view(request):
    return render(request, 'asd/main/list/main_list_4.html')  # 메인 목록4
def main_list_5_view(request):
    return render(request, 'asd/main/list/main_list_5.html')  # 메인 목록5

## 즐겨찾기
def bookmark_1_view(request):
    return render(request, 'asd/main/bookmark/bookmark_1.html')  # 즐겨찾기 1
def bookmark_2_view(request):
    return render(request, 'asd/main/bookmark/bookmark_2.html')  # 즐겨찾기 2
def bookmark_3_view(request):
    return render(request, 'asd/main/bookmark/bookmark_3.html')  # 즐겨찾기 3

## 바로가기
def quick_mypage_view(request):  # 마이페이지           
    return render(request, 'asd/main/mypage/user/mypage_mypage.html')
def quick_panel_view(request):  # 패널정보
    return render(request, 'asd/main/mypage/panel/mypage_panel.html')
def quick_recent_view(request):  # 최근접속 
    return render(request, 'asd/main/basic/main_recent.html')
def quick_contact_view(request):  # 문의방법
    return render(request, 'asd/main/basic/main_contact.html')

## 메인페이지 - 하단 (정보)
def down_privacy_view(request):  # 개인정보 처리방침        
    return render(request, 'asd/main/down/down_privacy.html')
def down_terms_view(request):  # 이용약관         
    return render(request, 'asd/main/down/down_terms.html')
def down_sitemap_view(request):  # 사이트맵        
    return render(request, 'asd/main/down/down_sitemap.html')

#---------------------------------------------------------------

## 회원가입
# 회원가입 창
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('로그인')  # 수정된 이름에 맞춰서 변경해 주세요.
    else:
        form = SignUpForm()
    
    return render(request, 'asd/user/basic/signup.html', {'form': form})

# 중복확인_아이디
@csrf_exempt
def signup_duplicate_id(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        if username and SignUp_User.objects.filter(username=username).exists():
            return JsonResponse({'exists': True})
        return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# 중복확인_이메일
@csrf_exempt
def signup_duplicate_email(request):
    if request.method == 'POST':
        useremail = request.POST.get('email', None)
        if useremail and SignUp_User.objects.filter(email=useremail).exists():
            return JsonResponse({'exists': True})
        return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

#---------------------------------------------------------------

## 로그인
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('id')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('메인페이지')  # 수정된 이름에 맞춰서 변경해 주세요.
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'asd/user/basic/login.html', {'form': form})

## 회원정보 찾기
def find_id_view(request):  # 아이디 찾기      
    return render(request, 'asd/user/find/find_id.html')
def find_pw_view(request):  # 비밀번호 찾기      
    return render(request, 'asd/user/find/find_pw.html')

#---------------------------------------------------------------

## 마이페이지

## 마이페이지 홈
@login_required
def mypage_mypage_view(request):
    return render(request, 'asd/mypage/user/mypage_mypage.html')

## 마이페이지 - 회원
# 회원정보 조회
@login_required
def search_user_view(request):
    return render(request, 'asd/mypage/user/search_user.html')

# 회원정보 수정 - 본인확인(비밀번호 입력)
@login_required
def confirm_pw_user_view(request):
    return render(request, 'asd/mypage/user/confirm_pw_user.html')

# 회원정보 수정 - 수정 페이지
@login_required
def modify_user_view(request):
    return render(request, 'asd/mypage/user/modify_user.html')


## 마이페이지 - 패널

# 패널정보조회
@login_required
def search_panel_view(request):
    return render(request, 'asd/mypage/panel/search_panel.html')

#본인확인_패널
@login_required
def confirm_pw_panel_view(request):
    return render(request, 'asd/mypage/panel/confirm_pw_panel.html')

#패널정보수정
@login_required
def modify_panel_view(request):
    return render(request, 'asd/mypage/panel/modify_panel.html')


#---------------------------------------------------------------
