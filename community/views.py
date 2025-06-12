from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommunityForm
from .models import Community, Post


def communities_list(request):
    Communities = Community.objects.all()
    return render(request, "communities/list.html" ,{"communities": Communities})

def community_create(request):
    form = CommunityForm()

    if request.method == "POST":
        form = CommunityForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            admin = request.user
            Community.objects.create(name=name, description=description, admins=admin)

    return render(request, "communities/create.html", {"form": form})


def community_edit(request, pk):
    community = get_object_or_404(Community, pk=pk)
    form = CommunityForm(instance=community)
    if request.method == "POST":
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            old = form.save()
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            old.name = name
            old.description = description
            old.save()
            return redirect("index")

        else:
            form = CommunityForm(instance=community)
    return render(request, "communities/edit.html", {"form": form})


