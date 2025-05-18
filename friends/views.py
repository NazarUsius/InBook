from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import CustomUser
from friends.models import Friends


def FriendsList(request):
    friends = Friends.objects.filter(person_one=request.user, accepted=True)
    context = {
        'friends': friends
    }
    return render(request, "friends/list.html", context)

def FriendsRequest(request, second: str):
    secon = get_object_or_404(CustomUser, username=second)
    Friends.objects.create(person_one=request.user, person_two=secon)
    return redirect("index")

def FriendsRequestAccept(request, iniciator:int):
    f_request = get_object_or_404(Friends, person_one=iniciator)
    f_request.accepted = True
    f_request.save()
    return redirect("friends_list")


