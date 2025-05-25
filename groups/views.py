from django.shortcuts import render, get_object_or_404

from .forms import GroupForm
from .models import Group


# Create your views here.
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
            Group.objects.create(name=form.cleaned_data["name"], description=form.cleaned_data["description"])
            return redirect("group_list")

    return render(request, "groups/add.htnl", {"form": form})


