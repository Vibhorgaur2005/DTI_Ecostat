from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('', views.home, name='home'),
    path("signup/",views.signup_view, name="signup"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("login/",views.login_view, name="login"),
    path('about/',views.about, name='about'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('sustainability-score/', views.sustainability_score, name='sustainability_score'),
    path('profile/', views.profile, name='profile'),
    path('community-insights/', views.community_insights, name='community_insights'),
    path('logout/', views.logout_page, name='logout'),
    path('communities/', views.community_insights, name='community_insights'),
    path('sustainability_calculator/', views.sustainability_calculator, name='sustainability_calculator'),
    path('community-insights/', views.community_insights_all, name='community_insights_all'),
    path('community-insights/<str:community>/', views.community_insights_detail, name='community_insights_detail'),
    path('calculate/', views.sustainability_calculator, name='sustainability_calculator'),
    ]
