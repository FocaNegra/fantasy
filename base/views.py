from re import I
from django.shortcuts import render, redirect
from django.http import HttpResponse
from base.custom_functions.fcf_functions import get_groups_from_category

from base.custom_functions.insert_functions import insert_calendar
from .models import  League, Calendar, Region, Region_Group, Region_Team, User_League
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .custom_functions.admin_functions import get_calendar, get_players, get_region_groups, get_teams_from_groups, get_player_list_via_url
from .custom_functions.insert_functions import insert_calendar, insert_players, insert_region_groups, insert_region_teams
from .custom_functions.fcf_competitions_to_add import *

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

def onboard_league(request):
    context = {}
    return render(request, 'base/onboard_league.html', context)


def join_league(request):
    if request.POST.get('action') == "Unirse a la liga":
        pass
    context = {}
    return render(request, 'base/join_league.html', context)

def create_league(request):
    region = Region.objects.get(id=1)
    context = {}
    player_list = []
    category = "TERCERA CATALANA"
    group_str = "GRUP 6"
    team_id = None
    league_name = ""
    region_category = Region_Group.objects.filter(category=category)
    region_group = region_category.get(group_name=group_str)
    teams = Region_Team.objects.filter(region_group=region_group).all()

    if request.method == 'POST':
        
        if "team_id" in request.POST:
            team_id = int(request.POST.get('team_id'))
        if "league_name" in request.POST:
            league_name = request.POST.get('league_name')
        if request.POST.get('action') == "Previsualizar equipo":
            team = Region_Team.objects.get(id=str(team_id))
            player_list = get_player_list_via_url(team.team_url)
        if request.POST.get('action') == "Crear liga":
            team_id = request.POST.get('team_id')
            region_team = Region_Team.objects.get(id=team_id)
            name = request.POST.get('league_name')
            status = 'active'

            if len(name) >= 1:
                league = League.objects.create(
                    name = name,
                    host = request.user,
                    region_team = region_team,
                    status = status,
                )
                u_l = User_League(
                    user = request.user,
                    league = league,
                    user_permission = 'admin'
                )
                u_l.save()
                return redirect('home')
    
    
    context = {'region_group': region_group, 'teams':teams, 'team_id': team_id, 'league_name': league_name, 'player_list': player_list}
    return render(request, 'base/create_league.html', context)


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
                if option == 'region_teams':
                    fcf_region = Region.objects.get(name='fcf')
                    grouplist_to_add = get_region_groups(competitions_to_add3, fcf_region)
                    insert_region_groups(grouplist_to_add, fcf_region)
                    insert_region_teams(get_teams_from_groups(grouplist_to_add))
    calendar = Calendar.objects.filter(league=league)                            
    context = {'league': league, 'calendar': calendar}
    return render(request, 'base/control_league.html', context)

