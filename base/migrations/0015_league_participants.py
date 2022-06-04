# Generated by Django 4.0.5 on 2022-06-04 15:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0014_user_league_date_joined_user_league_last_login_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', through='base.User_League', to=settings.AUTH_USER_MODEL),
        ),
    ]
