document.addEventListener('DOMContentLoaded', function() {
    let buttons = document.querySelectorAll('[id^="category_"]');

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            buttons.forEach(function(btn) {
                btn.classList.remove('active');
            });

            this.classList.add('active');

            localStorage.setItem('activeLink', this.id);
        });
    });
    const activeLinkId = localStorage.getItem('activeLink');
    if (activeLinkId) {
        document.getElementById(activeLinkId).classList.add('active');
    }
});
