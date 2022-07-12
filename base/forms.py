from ast import alias
from dataclasses import fields
from django import forms
from django.forms import ModelForm, Widget
from .models import Calendar, Player

class CalendarForm(ModelForm):
    class Meta:
        model = Calendar
        fields = '__all__'


class PlayerForm(ModelForm):
    error_css_class = 'error-field'
    required_css_class = "required-field"
    alias = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "alias"}))
    position = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "position"}))
    jersey_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "jersey_number"}))    
    match_report_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "match_report_name"}))

    class Meta:
        model = Player
        fields = ["match_report_name","alias", "position", "jersey_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ''
            if field == "match_report_name":
                self.fields["match_report_name"].widget.attrs['readonly'] = True
    
    def clen_match_report_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sku
        else:
            return self.cleaned_data['sku']

        # self.fields["alias"].label = ''
        # self.fields["position"].label = ''
        # self.fields["jersey_number"].label = ''
        # self.fields["match_report_name"].widget.attrs['readonly'] = True
