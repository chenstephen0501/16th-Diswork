// document.addEventListener("DOMContentLoaded", function() {
//     let carousel = document.querySelector('.aaa');
//     if (carousel) {
//         let options = {
//             infinite: true,
//             slidesToShow: 3,
//             slidesToScroll: 1,
//             autoplay: true,
//             autoplaySpeed: 1000,
//         };
//         new Slick(carousel, options);
//     }
// });

$('.slick-carousel').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows:false,
    dots:false,
    autoplay: true,
    autoplaySpeed: 1000,
    autoplayHoverPause:true,
    cssEase:"ease-out",
})