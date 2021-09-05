from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, fields
from app.models import TaskModel

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = '__all__'
