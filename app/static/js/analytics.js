const carousel = document.querySelector(".ana-scroll-card");

const arrowBtns = document.querySelectorAll(".flexy1 i");

function getElementWidth(element) {
  let card = document.querySelector(element);
  let styles = window.getComputedStyle(card);
  let width = styles.getPropertyValue("width");
  return parseFloat(width);
}

arrowBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    let scrollElementWidth = getElementWidth(".scroll-element");
    carousel.scrollLeft +=
      btn.id === "left" ? -scrollElementWidth : scrollElementWidth;
  });
});

let isMouseDown = false,
  startX,
  startScrollLeft;

const mouseDown = (e) => {
  isMouseDown = true;
  carousel.classList.add("dragging");
  startX = e.pageX;
  startScrollLeft = carousel.scrollLeft;
};

const mouseUp = () => {
  isMouseDown = false;
  carousel.classList.remove("dragging");
};

const dragging = (e) => {
  if (!isMouseDown) return;
  carousel.scrollLeft = startScrollLeft - (e.pageX - startX);
};

document.addEventListener("mouseup", mouseUp);
carousel.addEventListener("mousedown", mouseDown);
carousel.addEventListener("mousemove", dragging);
