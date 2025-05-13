from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed

from accounts.models import CustomUser

from .forms import UserProfileForm


def ProfileView(request, username: str):
    user = CustomUser.objects.get(username=username)
    return render(request, 'profiles/profile.html', {'user': user})


@login_required
def ChangeProfileView(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'profiles/edit_profile.html', context)
