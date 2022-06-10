from django.contrib import admin

# Register your models here.

from .models import League, Player, Region, Region_Team, User_League, Calendar, Region_Group, Region_Team

admin.site.register(League)
admin.site.register(Player)
admin.site.register(Region)
admin.site.register(Calendar)
admin.site.register(User_League)
admin.site.register(Region_Group)
admin.site.register(Region_Team)
