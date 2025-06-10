self.addEventListener("push", (event) => {
  const data = event.data.json();
  self.registration.showNotification(data.title, {
    body: data.body,
    icon: "/static/icons/icon.png", // или другой путь к иконке
  });
});
