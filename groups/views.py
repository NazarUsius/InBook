from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import GroupForm
from .models import Group, GroupMessage


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


def group_leave(request, group_id: int):
    group = get_object_or_404(Group, pk=group_id)

    if not group.is_member(request.user):
        messages.info(request, "You are not a member of this group.")
    else:
        group.members.remove(request.user)
        messages.success(request, f"You have successfully left the group: {group.name}")

    return redirect("group_detail", group_id=group_id)

def group_send_message(request, group_id: int):
    group = get_object_or_404(Group, pk=group_id)
    
    # Check if user is a member of the group
    if not group.is_member(request.user):
        messages.error(request, "You must be a member of this group to send messages.")
        return redirect("group_detail", group_id=group_id)
    
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            # Create the message
            GroupMessage.objects.create(
                group=group,
                user=request.user,
                content=content
            )
            messages.success(request, "Message sent successfully!")
        else:
            messages.error(request, "Message cannot be empty.")
    
    return redirect("group_detail", group_id=group_id)
