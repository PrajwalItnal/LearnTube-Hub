from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login, name = 'login'),
    path('user/profile/<str:username>/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('user/upload_course/', views.upload_course, name='upload_course'),
    path('post/<str:username>/', views.course_list, name='course_list'),
]