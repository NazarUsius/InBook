document.addEventListener("DOMContentLoaded", async () => {
  try {
    const registration = await navigator.serviceWorker.register("/static/js/sw.js");
    console.log("Service Worker зарегистрирован:", registration);

    console.log("Notification.permission:", Notification.permission);
    console.log(window.location.pathname)

    if (window.location.pathname === '/accounts/login/' || window.location.pathname === '/accounts/register') {
      console.log("Пользователь на экране логина/регистрации, пропускаю сообщение")
    } else {
       if (Notification.permission === "default") {
      setTimeout(() => {
        const banner = document.getElementById("notify-banner");
        if (!banner) {
          console.error("Баннер не найден");
          return;
        }
        banner.classList.remove("hidden");

        const yesBtn = document.getElementById("notify-yes");
        const noBtn = document.getElementById("notify-no");

        yesBtn.addEventListener("click", async () => {
          const permission = await Notification.requestPermission();
          if (permission !== "granted") {
            console.log("Пользователь не разрешил уведомления");
            banner.classList.add("hidden");
            return;
          }

          try {
            const subscription = await registration.pushManager.subscribe({
              userVisibleOnly: true,
              applicationServerKey: urlBase64ToUint8Array(
                "BH032alQmiGOOavyoVinw2RxELcnbjVVSeSuHF3ZXbjMJnX41Lbe0W78NbqVUmpj7Pmw8ygCtGIix5DpByVNjF8"
              ),
            });
            console.log("Подписка:", subscription);

            const response = await fetch("/subscribe/", {
              method: "POST",
              body: JSON.stringify(subscription),
              headers: { "Content-Type": "application/json" },
            });

            const result = await response.json();
            console.log("Ответ сервера:", result);
          } catch (err) {
            console.error("Ошибка подписки:", err);
          }

          banner.classList.add("hidden");
        });

        noBtn.addEventListener("click", () => {
          banner.classList.add("hidden");
          console.log("Пользователь отказался от подписки");
        });
      }, 3000); // таймер 3 секунды

    } else if (Notification.permission === "granted") {
      console.log("Разрешение уже получено — можно подписывать сразу (если нужно)");
      // Здесь можно подписываться сразу, если нужно
    } else {
      console.log("Пользователь запретил уведомления");
    }
    }


  } catch (err) {
    console.error("Ошибка регистрации Service Worker:", err);
  }
});

// Вспомогательная функция для VAPID ключа
function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/\-/g, "+").replace(/_/g, "/");
  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map((char) => char.charCodeAt(0)));
}
