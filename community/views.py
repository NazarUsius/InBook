from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommunityForm, CommentForm
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
            community = form.save(commit=False)
            community.save()
            community.admins.add(request.user)
            return redirect('communities_list')

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
            form.save()
            return redirect("communities_list")
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
    if request.user not in community.members.all():
        community.members.add(request.user)
    return redirect("communities_list")


@login_required
def community_leave(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if request.user not in community.members.all():
        community.members.remove(request.user)
    return redirect("communities_list")

@login_required
def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    is_member = request.user in community.members.all()
    is_admin = request.user in community.admins.all()
    posts = Post.objects.filter(community=community).prefetch_related('comments')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('community_detail', pk=community.pk)
    else:
        form = CommentForm()

    return render(request, "communities/detail.html", {
        "community": community,
        "is_member": is_member,
        "is_admin": is_admin,
        "posts": posts,
        "comment_form": form,
    })


@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.dislikes.remove(user)
        post.likes.add(user)

    return redirect('community_detail', pk=post.community.pk)



@login_required
def post_dislike(request,  post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.dislikes.all():
        post.dislikes.remove(user)
    else:
        post.likes.remove(user)
        post.dislikes.add(user)
    return redirect('community_detail', pk=post.community.pk)




