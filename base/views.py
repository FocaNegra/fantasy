from re import I
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import League
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Usuario no existe")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")


    context = {}
    return render(request, 'base/login_register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    leagues = League.objects.all()
    context = {'leagues':leagues}
    return render(request, 'base/home.html', context)

def league(request, pk):
    league = League.objects.get(id=pk)
    context = {'leagues':league}
    return render(request, 'base/league.html', context)
