from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('support', views.support_view, name='support'),
    path('faqs', views.faqs_view, name='faqs'),
    path('about', views.about_view, name='about'),
    path('settings', views.settings_view, name='settings'),
    path('upload', views.upload_view, name='upload'),
    path('follow', views.follow_view, name='follow'),
    path('likepost', views.likepost_view, name='likepost'),
    path('profile/<str:user>', views.profile_view, name='profile'),
]