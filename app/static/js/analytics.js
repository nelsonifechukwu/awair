const carousel = document.querySelector(".ana-scroll-card");

const dragging = (e) => {
    carousel.scrollLeft = e.pageX;
}

carousel.addEventListener ("mousemove", dragging);