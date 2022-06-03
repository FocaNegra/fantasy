from asyncio.windows_events import NULL
from email.policy import default
from django.db import models
from django.forms import BooleanField
from django.contrib.auth.models import User

# Create your models here.


class Region(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name



class League(models.Model):

    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    is_active = BooleanField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User_League(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username}_{self.league}'
