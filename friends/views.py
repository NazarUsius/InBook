from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import CustomUser
from friends.models import Friends


def friends_list(request):
    friends = Friends.objects.filter(person_one=request.user, accepted=True)
    context = {
        'friends': friends
    }
    return render(request, "friends/list.html", context)

def friends_request(request, second: int):
    secon = get_object_or_404(CustomUser, pk=second)
    Friends.objects.create(person_one=request.user, person_two=secon)
    return redirect("index")

def friends_request_accept(request, iniciator:int):
    f_request = get_object_or_404(Friends, person_one=iniciator)
    f_request.accepted = True
    f_request.save()
    return redirect("friends_list")

def friends_request_decline(request, iniciator:int):
    f_request = get_object_or_404(Friends, person_one=iniciator)
    f_request.delete()
    return redirect("friends_list")

def friends_delete(request, second: int):
    friend = get_object_or_404(Friends, person_two=second)
    friend.delete()
    return redirect("friends_list")

