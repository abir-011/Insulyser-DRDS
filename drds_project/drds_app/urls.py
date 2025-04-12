from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login', views.login_view, name='login_post'),
    path('logout', views.logout_view, name='logout'),
    path('welcome', views.welcome_view, name='welcome'),
    path('home', views.home_view, name='home'),
    path('upload', views.upload_view, name='upload'),
    path('wait', views.wait_view, name='wait'),
    path('about', views.about_view, name='about'),
    path('contact', views.contact_view, name='contact'),
]
