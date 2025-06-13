from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommunityForm
from .models import Community, Post


@login_required
def communities_list(request):
    Communities = Community.objects.all()
    return render(request, "communities/list.html" ,{"communities": Communities})

@login_required
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


@login_required
def community_edit(request, pk):
    community = get_object_or_404(Community, pk=pk)
    form = CommunityForm(instance=community)

    if request.user not in community.admins.all():
        return HttpResponseForbidden("You are not allowed to edit this community.")

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


@login_required
def community_delete(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if request.user not in community.admins.all():
        return HttpResponseForbidden("You are not admin of this community.")

    if request.method == "POST":
        community.delete()
        return redirect("communities_list")

    return render(request, "communities/delete.html", {"community": community})


@login_required
def community_join(request, pk):
    community = get_object_or_404(Community, pk=pk)
    community.members.add(request.user)
    community.save()
    return redirect("communities_list")


@login_required
def community_leave(request, pk):
    community = get_object_or_404(Community, pk=pk)
    community.members.remove(request.user)
    community.save()
    return redirect("communities_list")

@login_required
def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    is_member = request.user.is_authenticated and request.user in community.members.all()
    is_admin = request.user.is_authenticated and request.user in community.admins.all()
    posts = Post.objects.filter(community=community)

    return render(request, "communities/detail.html", {
        "community": community,
        "is_member": is_member,
        "is_admin": is_admin,
        "posts": posts,
    })



