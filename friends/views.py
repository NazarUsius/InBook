from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import CustomUser
from friends.models import Friends, FriendRequest


def FriendsList(request):
    friends = Friends.objects.filter(person_one=request.user)
    context = {
        'friends': friends
    }
    return render(request, "friends/list.html", context)

def FriendsRequest(request, second: str):
    secon = get_object_or_404(CustomUser, username=second)
    FriendRequest.objects.create(iniciator=request.user, acceptor=secon)
    return redirect("index")