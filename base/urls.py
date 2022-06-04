from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.LogoutUser, name="logout"),
    path('', views.home, name="home"),
    path('league/<str:pk>/', views.league, name="league"),
]