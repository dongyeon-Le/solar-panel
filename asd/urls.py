from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView
from .views import CustomPasswordResetDoneView

urlpatterns = [
    # 메인 페이지
    path('', views.main_view, name='메인페이지'),
    
    # 메인 페이지 - 상단 (목록)
    path('main_list_1/', views.main_list_1_view, name='메인 목록1'),
    path('main_list_2/', views.main_list_2_view, name='메인 목록2'),
    path('main_list_3/', views.main_list_3_view, name='메인 목록3'),
    path('main_list_4/', views.main_list_4_view, name='메인 목록4'),
    path('main_list_5/', views.main_list_5_view, name='메인 목록5'),
    
    # 메인 페이지 - 하단 (정보)
    path('privacy/', views.down_privacy_view, name='개인정보 처리방침'),
    path('terms/', views.down_terms_view, name='이용약관'),
    path('sitemap/', views.down_sitemap_view, name='사이트맵'),
    
    # 즐겨찾기
    path('bookmark_1/', views.bookmark_1_view, name='즐겨찾기 1'),
    path('bookmark_2/', views.bookmark_2_view, name='즐겨찾기 2'),
    path('bookmark_3/', views.bookmark_3_view, name='즐겨찾기 3'),
    
    # 바로가기
    path('recent/', views.quick_recent_view, name='최근접속'),
    path('contact/', views.quick_contact_view, name='문의방법'),
    
    # 회원가입
    path('signup/', views.signup_view, name='회원가입'),
    path('signup/duplicate/id', views.check_id_duplicate, name='아이디 중복확인'),
    path('signup/duplicate/email', views.check_email_duplicate, name='이메일 중복확인'),

    # 로그인
    path('login/', views.login_view, name='로그인'),
    path('logout/', views.logout_view, name='로그아웃'),

    # 회원정보 찾기
    path('find/', views.find_view, name='회원정보 찾기'),
    path('find_id/', views.find_id_view, name='아이디 찾기'),
    path('find_pw/', CustomPasswordResetView.as_view(), name='비밀번호 찾기'),
    path('reset/<uidb64>/<token>/s', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # 비밀번호 초기화 인증
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'), # 비밀번호 초기화 실행 
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), # 비밀번호 초기화 완료
    
    # 마이페이지 - 회원
    path('mypage/', views.mypage_view, name='마이페이지'),
    path('search_user/', views.search_user_view, name='회원정보조회'),
    path('modify_user/', views.modify_user_view, name='회원정보수정'),
    path('validate_password/', views.validate_password, name='본인확인 인증'),
    path('confirm_pw_user/', views.confirm_pw_user_view, name='본인확인 완료'),

    # 마이페이지 - 패널
    path('search_panel/', views.search_panel_view, name='패널정보 조회'),
    path('modify_panel/<int:panel_id>/', views.modify_panel_view, name='패널정보 수정'),
    path('delete_panel/<int:panel_id>/', views.delete_panel_view, name='패널정보 삭제'),
    path('save_panel/', views.save_panel_view, name='패널정보 저장'),
    path('input_panel/', views.input_panel_view, name='패널정보 입력'),

    path('find_id/', views.find_id_view, name='find_id'),

    # path('analysis/', views.map_result, name='분석결과'),

    path('repair_service/', views.repair_service_view, name='유지보수 서비스'),
    path('repair_result/', views.repair_service_result, name='유지보수 결론'),

    path('main_panel/<int:panel_id>', views.main_panel, name='메인패널 설정'),

     # 공지사항
    
    path('notice/1/',views.main_notice_1_view, name='공지사항1'),
    path('notice/2/',views.main_notice_2_view, name='공지사항2'),
    path('event/1/',views.main_event_1_view, name='이벤트1'),
    path('event/2/',views.main_event_2_view, name='이벤트2'),

    
    
]

