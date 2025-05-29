document.addEventListener("DOMContentLoaded", async () => {
  const button = document.getElementById("subscribe-btn");

  if (!button) {
    console.error("Кнопка не найдена!");
    return;
  }

  button.addEventListener("click", async () => {
    try {
      const permission = await Notification.requestPermission();

      if (permission !== "granted") {
        console.log("Пользователь не разрешил уведомления");
        return;
      }

      const registration =
        await navigator.serviceWorker.register("/static/js/sw.js");
      console.log("Service Worker зарегистрирован:", registration);

      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(
          "BNJ-m3pc749xHCFI3SChhfPuceBA4yoXtjiiufN4r5yEfQHHErdxsTKeoc549Hr54SkS_IkvJLh4-vg3LqSf4-I",
        ),
      });

      console.log("Подписка:", subscription);

      const response = await fetch("/subscribe/", {
        method: "POST",
        body: JSON.stringify(subscription),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const result = await response.json();
      console.log("Ответ сервера:", result);
    } catch (err) {
      console.error("Ошибка подписки:", err);
    }
  });
});

// Вспомогательная функция
function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, "+")
    .replace(/_/g, "/");

  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map((char) => char.charCodeAt(0)));
}
