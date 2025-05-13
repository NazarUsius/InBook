from django.shortcuts import render

from accounts.models import CustomUser


def ProfileView(request, username: str):
    user = CustomUser.objects.get(username=username)
    return render(request, 'profiles/profile.html', {'user': user})
