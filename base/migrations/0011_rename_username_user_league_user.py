# Generated by Django 4.0.5 on 2022-06-29 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_region_team_region_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_league',
            old_name='username',
            new_name='user',
        ),
    ]
