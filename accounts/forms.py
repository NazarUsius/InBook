from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'gender', 'avatar', 'birth_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Логін',
            'email': 'Електронна пошта',
            'gender': 'Стать',
            'avatar': 'Аватар',
            'birth_date': 'Дата народження',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Користувач з такою поштою вже існує.")
        return email
from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'gender', 'avatar', 'birth_date')