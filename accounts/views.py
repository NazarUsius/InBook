from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def RegisterView(request):
    form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
