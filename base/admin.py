from django.contrib import admin

# Register your models here.

from .models import League, Region, User_League

admin.site.register(League)
admin.site.register(User_League)
admin.site.register(Region)
