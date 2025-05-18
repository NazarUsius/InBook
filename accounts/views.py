from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomCreationForm


def RegisterView(request):
    form = CustomCreationForm()
    if request.method == 'POST':
        form = CustomCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.user.is_authenticated:
                return redirect("index")
    return render(request, 'accounts/register.html', {'form': form})
