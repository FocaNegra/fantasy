from re import I
from django.shortcuts import render
from django.http import HttpResponse
from .models import League

# Create your views here.


def home(request):
    leagues = League.objects.all()
    context = {'leagues':leagues}
    return render(request, 'base/home.html', context)

def league(request, pk):
    league = League.objects.get(id=pk)
    context = {'leagues':league}
    return render(request, 'base/league.html', context)
