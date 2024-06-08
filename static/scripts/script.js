// document.addEventListener('DOMContentLoaded', function() {
//     let buttons = document.querySelectorAll('[id^="category_"]');

//     buttons.forEach(function(button) {
//         button.addEventListener('click', function() {
//             buttons.forEach(function(btn) {
//                 btn.classList.remove('active');
//             });

//             this.classList.add('active');

//             localStorage.setItem('activeLink', this.id);
//         });
//     });

//     let activeLinkId = localStorage.getItem('activeLink');
//     console.log(activeLinkId);
//     if (activeLinkId) {
//         document.getElementById(activeLinkId).classList.add('active');
//     }
// });

const carousel = document.querySelector(".ads-carousel")
const slides = carousel.querySelectorAll(".slide")
const track = carousel.querySelector(".track")
console.log(slides.length)
function setupSlides() {
    const w = track.clientWidth

    slides.forEach((slide, i) => {
        slide.style.left = `${i * w}px`
    })
    adsInterval(0, w)
}

function adsInterval(index, w) {
    let slideIndex = index;
    
    setInterval(function() {
        slideIndex = (slideIndex + 1) % slides.length;
        track.style.transform = `translateX(-${slideIndex * w}px)`
    }, 3000)
    console.log("test")
}

setupSlides()


