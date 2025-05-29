from pywebpush import webpush, WebPushException
from notifications.models import WebPushSubscription  # или путь к твоей модели
import json

import os
from dotenv import load_dotenv

load_dotenv()


VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_CLAIMS = {
    "sub": "mailto:nazar.gadzhalov@gmail.com"  # замени на свою почту
}

def send_push_notification(title, body):
    payload = {
        "title": title,
        "body": body
    }

    subscriptions = WebPushSubscription.objects.all()

    for sub in subscriptions:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth,
                    }
                },
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            print("Уведомление отправлено:", sub.endpoint)
        except WebPushException as ex:
            print("Ошибка отправки:", repr(ex))
