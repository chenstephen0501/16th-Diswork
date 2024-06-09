function setupCarousel(carousel) {

    const slides = carousel.querySelectorAll(".slide")
    const track = carousel.querySelector(".track")
    function setupSlides() {
        const w = track.clientWidth

        slides.forEach((slide, i) => {
            slide.style.left = `${i * w}px`
        })
        adsInterval(0, w)
    }

    function adsInterval(index, w) {
        let slideIndex = index;

        setInterval(function () {
            slideIndex = (slideIndex + 1) % slides.length;
            track.style.transform = `translateX(-${slideIndex * w}px)`
        }, 5000)
    }
    setupSlides()
}

document.querySelectorAll(".ads-carousel").forEach(setupCarousel)


