from django.contrib import admin

# Register your models here.

from .models import Calendar, League, Calendar, Player, Region, User_League

admin.site.register(League)
admin.site.register(Player)
admin.site.register(Region)
admin.site.register(Calendar)
admin.site.register(User_League)
