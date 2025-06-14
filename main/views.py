from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from community.models import Post, Community


@login_required
def index(request):
    # Отримати всі спільноти, де користувач є учасником
    user_communities = request.user.communities.all()

    # Отримати пости з цих спільнот, останні першими
    posts = Post.objects.filter(community__in=user_communities).order_by('-created_at')[:20]  # останні 20

    return render(request, 'index.html', {'posts': posts})
