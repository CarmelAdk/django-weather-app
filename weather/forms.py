from django.forms import ModelForm, TextInput
from .models import City
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nom de la ville'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super(CityForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CityForm, self).save(commit=False)
        if self.user:
            instance.user = self.user 
        if commit:
            instance.save()
        return instance


class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())