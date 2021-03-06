from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.LogoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('onboard_league/', views.onboard_league, name="onboard_league"),
    path('join_league/', views.join_league, name="join_league"),
    path('create_league/', views.create_league, name="create_league"),
    path('', views.home, name="home"),
    path('more/', views.more, name="more"),
    path('control/', views.control, name="control"),
    path('control/league/<str:pk>/', views.control_league, name="control_league"),
    path('league/<str:pk>/', views.league, name="league"),
    path('players/', views.players, name="players"),
    path('calendars/', views.calendars, name="calendars"),    
    path('match_reports/<str:pk>/', views.match_reports, name="match_report"),
]


