from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Friends, Subscription
from django.contrib.auth import get_user_model
from notifications.utils import send_push_notification

User = get_user_model()

@login_required
def friends_list(request):
    # Получаем все друзья где пользователь - person_one или person_two и accepted=True
    friends = Friends.objects.filter(
        Q(person_one=request.user) | Q(person_two=request.user),
        accepted=True
    )
    context = {'friends': friends}
    return render(request, "friends/list.html", context)


@login_required
def friends_request(request, second: int):
    if second == request.user.id:
        messages.error(request, "Ви не можете надіслати запит собі.")
        return redirect("index")

    secon = get_object_or_404(User, pk=second)

    exists = Friends.objects.filter(
        (Q(person_one=request.user) & Q(person_two=secon)) |
        (Q(person_one=secon) & Q(person_two=request.user))
    ).exists()

    if exists:
        messages.info(request, "Запит на дружбу вже існує або ви вже друзі.")
        return redirect("index")

    Friends.objects.create(person_one=request.user, person_two=secon)
    send_push_notification(
        request.user,
        "Запрос на дружбу",
        f"{request.user.username} відправив(ла) вам запрос на дружбу"
    )
    messages.success(request, "Запит на дружбу надіслано.")
    return redirect("index")


@login_required
def friends_request_accept(request, initiator: int):
    # Поиск запроса на дружбу где инициатор отправил запрос текущему пользователю
    f_request = get_object_or_404(Friends, person_one_id=initiator, person_two=request.user, accepted=False)
    f_request.accepted = True
    f_request.save()
    messages.success(request, "Запит на дружбу прийнято.")
    return redirect("friends_list")


@login_required
def friends_request_decline(request, initiator: int):
    f_request = get_object_or_404(Friends, person_one_id=initiator, person_two=request.user, accepted=False)
    f_request.delete()
    messages.success(request, "Запит на дружбу відхилено.")
    return redirect("friends_list")


@login_required
def friends_delete(request, second: int):
    friend = Friends.objects.filter(
        (Q(person_one=request.user) & Q(person_two_id=second)) |
        (Q(person_one_id=second) & Q(person_two=request.user)),
        accepted=True
    ).first()

    if friend:
        friend.delete()
        messages.success(request, "Друг видалений.")
    else:
        messages.error(request, "Друг не знайдений.")
    return redirect("friends_list")


@login_required
def subscribe(request, user_id):
    if user_id == request.user.id:
        messages.error(request, "Неможливо підписатися на самого себе.")
        return redirect('profile', user_id=user_id)

    user_to_follow = get_object_or_404(User, id=user_id)

    subscription, created = Subscription.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    if created:
        messages.success(request, "Ви підписалися на користувача.")
    else:
        messages.info(request, "Ви вже підписані на цього користувача.")
    return redirect('profile', user_id=user_id)


@login_required
def unsubscribe(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    deleted, _ = Subscription.objects.filter(follower=request.user, following=user_to_unfollow).delete()

    if deleted:
        messages.success(request, "Ви відписалися від користувача.")
    else:
        messages.info(request, "Ви не були підписані на цього користувача.")
    return redirect('profile', user_id=user_id)


@login_required
def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    user_subscriptions = Subscription.objects.filter(follower=request.user).values_list('following_id', flat=True)

    friends_count = Friends.objects.filter(
        Q(person_one=profile_user) | Q(person_two=profile_user),
        accepted=True
    ).count()

    followers_count = Subscription.objects.filter(following=profile_user).count()

    following_count = Subscription.objects.filter(follower=profile_user).count()

    context = {
        'profile_user': profile_user,
        'user_subscriptions': list(user_subscriptions),
        'friends_count': friends_count,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'friends/profile.html', context)