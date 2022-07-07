from ast import alias
from dataclasses import fields
from turtle import width
from django import forms
from django.forms import ModelForm, Widget
from .models import Calendar, Player

class CalendarForm(ModelForm):
    class Meta:
        model = Calendar
        fields = '__all__'


class PlayerForm(ModelForm):
    error_css_class = 'error-field'
    required_css_class = ""
    alias = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "alias"}))
    position = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "position"}))
    jersey_number = forms.CharField(label='', widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "jersey_number"}))

    class Meta:
        model = Player
        fields = ["alias", "position", "jersey_number"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["alias"].label = ''
    #     self.fields["position"].label = ''
    #     self.fields["jersey_number"].label = ''
