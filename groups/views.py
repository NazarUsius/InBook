from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import GroupForm
from .models import Group


def group_list(request):
    groups = Group.objects.all()    # There I think must be ";"
    return render(request, "groups/list.html", {"groups": groups})


def group_detail(request, group_id: int):
    group = get_object_or_404(Group, pk=group_id)
    return render(request, "groups/detail.html", {"group": group})

def group_add(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("group_list")

    return render(request, "groups/add.html", {"form": form})


def group_join(request, group_id: int):
    group = get_object_or_404(Group, pk=group_id)

    if group.is_member(request.user):
        messages.info(request, "You are already a member of this group.")
    else:
        group.members.add(request.user)
        messages.success(request, f"You have successfully joined the group: {group.name}")

    return redirect("group_detail", group_id=group_id)
