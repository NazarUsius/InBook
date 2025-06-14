from pywebpush import webpush, WebPushException
from notifications.models import WebPushSubscription
from django.conf import settings
import json


def send_push_notification(user, title, body):
    subscription = WebPushSubscription.objects.filter(user=user).first()
    if not subscription:
        return

    payload = {
        "title": title,
        "body": body,
    }

    try:
        webpush(
            subscription_info={
                "endpoint": subscription.endpoint,
                "keys": {
                    "p256dh": subscription.p256dh,
                    "auth": subscription.auth
                }
            },
            data=json.dumps(payload),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims=settings.VAPID_CLAIMS
        )
    except WebPushException as ex:
        print("Web push failed: ", repr(ex))
