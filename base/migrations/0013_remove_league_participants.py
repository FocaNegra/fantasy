# Generated by Django 4.0.5 on 2022-06-04 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_remove_league_admins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='participants',
        ),
    ]