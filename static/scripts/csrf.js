document.addEventListener("htmx:configRequest", function (event) {
  const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
  if (csrfToken) {
    event.detail.headers["X-CSRFToken"] = csrfToken;
  }
});
