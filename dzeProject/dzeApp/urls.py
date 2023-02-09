
from django.contrib.auth import logout

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('success/', views.success, name='success'),
    path('send_email', views.send_email, name='send_email'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('send_comment', views.send_comment, name='send_comment'),


]
