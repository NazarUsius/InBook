from pywebpush import webpush, WebPushException
from notifications.models import WebPushSubscription
from django.conf import settings
import json
from urllib.parse import urlparse


def send_push_notification(user, title, body):
    subscription = WebPushSubscription.objects.filter(user=user).first()
    if not subscription:
        return

    payload = {
        "title": title,
        "body": body,
    }

    parsed_url = urlparse(subscription.endpoint)
    aud = f"{parsed_url.scheme}://{parsed_url.netloc}"

    vapid_claims = {
        "sub": "mailto:your_email@example.com",  # ваш email
        "aud": aud,
    }

    try:
        print(settings.VAPID_PRIVATE_KEY)
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
            vapid_claims=vapid_claims
        )
    except WebPushException as ex:
        print("Web push failed:", repr(ex))
