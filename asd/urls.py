from django.urls import path
from . import views

urlpatterns = [
    # 메인 페이지
    path('', views.main_view, name='메인페이지'),
    
    # 메인 페이지 - 상단 (목록)
    path('main_list_1/', views.main_list_1_view, name='메인 목록1'),
    path('main_list_2/', views.main_list_2_view, name='메인 목록2'),
    path('main_list_3/', views.main_list_3_view, name='메인 목록3'),
    path('main_list_4/', views.main_list_4_view, name='메인 목록4'),
    path('main_list_5/', views.main_list_5_view, name='메인 목록5'),
    
    # 즐겨찾기
    path('bookmark_1/', views.bookmark_1_view, name='즐겨찾기 1'),
    path('bookmark_2/', views.bookmark_2_view, name='즐겨찾기 2'),
    path('bookmark_3/', views.bookmark_3_view, name='즐겨찾기 3'),
    
    # 바로가기
    path('recent/', views.quick_recent_view, name='최근접속'),
    path('contact/', views.quick_contact_view, name='문의방법'),
    
    # 메인 페이지 - 하단 (정보)
    path('privacy/', views.down_privacy_view, name='개인정보 처리방침'),
    path('terms/', views.down_terms_view, name='이용약관'),
    path('sitemap/', views.down_sitemap_view, name='사이트맵'),
    
    # 회원가입
    path('signup/', views.signup_view, name='회원가입'),

    # 로그인
    path('login/', views.login_view, name='로그인'),
    
    # 회원정보 찾기
    path('find/', views.find_view, name='회원정보 찾기'),
    path('find_id/', views.find_id_view, name='아이디 찾기'),
    path('find_pw/', views.find_pw_view, name='비밀번호 찾기'),
    
    # 마이페이지 - 회원
    path('mypage/', views.mypage_view, name='마이페이지'),
    path('search_user/', views.search_user_view, name='회원정보조회'),
    path('modify_user/', views.modify_user_view, name='회원정보수정'),
    
    # 마이페이지 - 패널
    path('search_panel/', views.search_panel_view, name='패널정보조회'),
    path('modify_panel/', views.modify_panel_view, name='패널정보수정'),
    
]
