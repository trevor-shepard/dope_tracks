from django.forms.models import ModelForm
from django.forms import Form, ChoiceField
from .models import Group
from django import forms

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'