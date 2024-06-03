$(function() {
    $('[id^="category_"]').click(function() {
        $('[id^="category_"]').removeClass('active')
        $(this).addClass('active')
        localStorage.setItem('activeLink', $(this).attr('id'));
    });
    const activeLinkId = localStorage.getItem('activeLink');
    console.log(activeLinkId);
    if (activeLinkId) {
        $('#' + activeLinkId).addClass('active');
    }
})