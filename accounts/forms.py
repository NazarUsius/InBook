from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'gender', 'avatar', 'birth_date')