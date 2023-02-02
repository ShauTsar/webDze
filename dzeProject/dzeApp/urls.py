
from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('success/', views.success, name='success'),
    path('send_email', views.send_email, name='send_email'),
    path('register/', views.register, name='register'),


]
