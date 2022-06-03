from django.contrib import admin

# Register your models here.

from .models import League, Match_Report, Player, Region, User_League

admin.site.register(League)
admin.site.register(Player)
admin.site.register(Region)
admin.site.register(Match_Report)
