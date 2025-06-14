from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import WebPushSubscription
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def save_subscription(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            endpoint = data["endpoint"]
            p256dh = data["keys"]["p256dh"]
            auth = data["keys"]["auth"]

            # Сохраняем в БД
            WebPushSubscription.objects.create(user=request.user, endpoint=endpoint, p256dh=p256dh, auth=auth)

            return JsonResponse({"status": "ok"})
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({"error": "Missing fields or invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)



from django.http import JsonResponse
from .utils import send_push_notification

def notify_users(request):
    send_push_notification(
        request.user,
        "Привет!",
        "Сервис подключен, и готов к работе!")
    return JsonResponse({"status": "ok"})

