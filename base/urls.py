from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.LogoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('control/', views.control, name="control"),
    path('control/league/<str:pk>/', views.control_league, name="control_league"),
    path('league/<str:pk>/', views.league, name="league"),
    path('players/', views.league_players, name="league_players"),
]
