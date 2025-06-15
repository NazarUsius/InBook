import re
from django import template
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()

@register.filter
def render_mentions(text):
    print(text)
    def replace(match):
        username = match.group(1)
        try:
            user = User.objects.get(username=username)
            url = reverse('profile', args=[user.id])
            return f'<a href="{url}">@{escape(username)}</a>'
        except User.DoesNotExist:
            return f'@{escape(username)}'

    result = re.sub(r'@(\w+)', replace, text)
    return mark_safe(result)