# Generated by Django 4.0.5 on 2022-06-03 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_league_status_league_team_alias_player_match_report'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='macth_report_name',
            new_name='match_report_name',
        ),
    ]