from django.contrib import admin

from friends.models import Friends, FriendRequest

admin.site.register(Friends)
admin.site.register(FriendRequest)
