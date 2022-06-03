from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('league/<str:pk>/', views.league, name="league"),
]