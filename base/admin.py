from django.contrib import admin

# Register your models here.

from .models import League, Player, Region, User_League, Calendar

admin.site.register(League)
admin.site.register(Player)
admin.site.register(Region)
admin.site.register(Calendar)
admin.site.register(User_League)
