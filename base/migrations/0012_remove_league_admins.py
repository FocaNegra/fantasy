# Generated by Django 4.0.5 on 2022-06-04 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_rename_macth_report_name_player_match_report_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='admins',
        ),
    ]
