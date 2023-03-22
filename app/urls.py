from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name = 'register'),
    path('token', views.token, name='token'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),
    path('webcam', views.webcam, name="webcam"),
    path('process_frame', views.process_frame, name='process_frame'),
]