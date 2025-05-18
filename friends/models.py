from django.db import models
from django.conf import settings

class Friends(models.Model):
    person_one = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='person_one')
    person_two = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='person_two')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('person_one', 'person_two')

