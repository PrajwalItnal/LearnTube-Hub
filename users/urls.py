from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login_view, name = 'login'),
    path('user/profile/<str:username>/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('user/upload_course/', views.upload_course, name='upload_course'),
    path('post/<str:username>/', views.course_list, name='course_list'),
    path('course/<int:course_id>/save/', views.save_course, name='save_course'),
    path('course/<int:course_id>/unsave/', views.unsave_course, name='unsave_course'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    # Enrollment
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('course/<int:course_id>/update-view-time/', views.update_view_time, name='update_view_time'),
    # Certificates
    path('course/<int:course_id>/certificate/', views.generate_certificate, name='generate_certificate'),
    path('my-certificates/', views.my_certificates, name='my_certificates'),
    path('verify-certificate/<uuid:cert_uuid>/', views.verify_certificate, name='verify_certificate'),
    path('course/<int:course_id>/enrolled-students/', views.course_enrolled_students, name='course_enrolled_students'),
    path('validate-youtube-url/', views.validate_youtube_url, name='validate_youtube_url'),
]