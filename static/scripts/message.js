document.addEventListener('DOMContentLoaded', function () {
  let messagesDiv = document.getElementById('django-messages');
  if (messagesDiv) {
    let messages = messagesDiv.getElementsByClassName('message');
    for (let i = 0; i < messages.length; i++) {
      let message = messages[i].textContent || messages[i].innerText;
      let messageType = messages[i].className.split(' ')[1];

      let icon;
      if (messageType === 'error') {
        icon = 'error';
      } else if (messageType === 'success') {
        icon = 'success';
      }

      Swal.fire({
        text: message,
        icon: icon,
        confirmButtonColor: '#FE952A',
        customClass: {
          confirmButton: 'custom-confirm-button-class'
        }
      });
      messages[i].style.display = 'none';
    }
  }
});
