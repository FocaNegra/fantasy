from re import I
from django.shortcuts import render, redirect
from django.http import HttpResponse

from base.custom_functions.insert_functions import insert_calendar
from .models import  League, Calendar
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .custom_functions.admin_functions import get_calendar, get_players
from .custom_functions.insert_functions import insert_calendar, insert_players

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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


    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    context = {'form': form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ha ocurrido un error durante el proceso de registro.')

    return render(request, 'base/login_register.html', context)


def home(request):
    leagues = League.objects.all()
    context = {'leagues':leagues}
    return render(request, 'base/home.html', context)

def league(request, pk):
    league = League.objects.get(id=pk)
    context = {'leagues': league}
    return render(request, 'base/league.html', context)

def control(request):
    leagues = League.objects.order_by('id')[:5]
    league = {}

    if request.method == 'POST':
        league_id = request.POST.get('league')
        league = League.objects.get(id=league_id)
        
    context = {'leagues': leagues, 'league': league}
    return render(request, 'base/control.html', context)

def control_league(request, pk):
    league = League.objects.get(id=pk)
    calendar = Calendar.objects.filter(league=league)
    if request.method == 'POST':
        try:
            options = dict(request.POST)['control-options']
        except:
            options = []
        if options:
            for option in options:
                if option == 'calendar':
                    insert_calendar(get_calendar(league), league)
                if option == 'players':
                    insert_players(get_players(league), league)
    calendar = Calendar.objects.filter(league=league)                            
    context = {'league': league, 'calendar': calendar}
    return render(request, 'base/control_league.html', context)

