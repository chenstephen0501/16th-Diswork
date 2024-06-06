// $(function() {
//     $('[id^="category_"]').click(function() {
//         $('[id^="category_"]').removeClass('active')
//         $(this).addClass('active')
//         localStorage.setItem('activeLink', $(this).attr('id'));
//     });
//     const activeLinkId = localStorage.getItem('activeLink');
//     console.log(activeLinkId);
//     if (activeLinkId) {
//         $('#' + activeLinkId).addClass('active');
//     }
// })


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

    let activeLinkId = localStorage.getItem('activeLink');
    console.log(activeLinkId);
    if (activeLinkId) {
        document.getElementById(activeLinkId).classList.add('active');
    }
});
