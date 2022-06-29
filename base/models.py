from asyncio.windows_events import NULL
from email.policy import default
from unicodedata import category
from django.db import models
from django.forms import BooleanField
from django.contrib.auth.models import User

# Create your models here.


class Region(models.Model):
    name = models.CharField(max_length=40)
    url_schedule = models.CharField(max_length=40, blank=True, null=True)
    url_team = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

class Region_Group(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, null=True)
    group_name = models.CharField(max_length=100, null=True)
    group_url = models.CharField(max_length=300)
    standing_url = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.region}/{self.category}/{self.group_name}'


class Region_Team(models.Model):
    region_group = models.ForeignKey(Region_Group, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    alias = models.CharField(max_length=20, null=True)
    schedule_url = models.CharField(max_length=300, null=True)
    team_url = models.CharField(max_length=300, null=True)    

    def __str__(self):
        return f'{self.region_group}/{self.alias}'


class League(models.Model):

    name = models.CharField(max_length=200)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, through='User_League', related_name='participants', blank=True)
    region_team = models.ForeignKey(Region_Team, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, default="active")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)
    match_report_name = models.CharField(max_length=200)
    jersey_number = models.CharField(max_length=3, null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        if self.alias == '' or self.alias == None:
            return f"{self.name} {self.last_name}"
        else:
            return f'{self.name} "{self.alias}" {self.last_name}'

class Calendar(models.Model):
    week = models.CharField(max_length=4)
    season = models.CharField(max_length=12)
    game_date = models.DateTimeField()
    url = models.CharField(max_length=200)
    result = models.CharField(max_length=12, null=True)
    status = models.CharField(max_length=30)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    oponent = models.CharField(max_length=200)
    hosting = models.CharField(max_length=8)
    team_enddate = models.DateTimeField()
    punctuation_enddate = models.DateTimeField()
    last_update = models.DateTimeField(auto_now=True)
    next_update = models.DateTimeField()

    def __str__(self):
        return f'{self.league}_{self.season}_{self.week}'


class User_League(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    user_permission = models.CharField(max_length=25, null=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user.id}_{self.league.id}'



