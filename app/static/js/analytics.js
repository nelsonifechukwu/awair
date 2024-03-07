const carousel = document.querySelector(".ana-scroll-card");
const arrowBtns = document.querySelectorAll(".flexy1 i");
const lbutton = document.getElementById("button-left");
let scrollElementWidth = getElementWidth(".scroll-element");

function getElementWidth(element) {
  let card = document.querySelector(element);
  let styles = window.getComputedStyle(card);
  let width = styles.getPropertyValue("width");
  return parseInt(width);
}
arrowBtns.forEach((btn) => {
  btn.onclick = () => {
    carousel.scrollLeft +=
      btn.id === "button-left" ? -scrollElementWidth : scrollElementWidth;
    carousel.scrollLeft < 0 ? (carousel.scrollLeft = 0) : 0;
    // console.log(`SL1${carousel.scrollLeft}`);
    setTimeout(buttonState, 255); //Delay buttonState call to allow .scrollLeft to update after the eventlistener is triggered
  };
});

let buttonState = () => {
  parseInt(carousel.scrollLeft) > 0
    ? (lbutton.style.display = "block")
    : (lbutton.style.display = "none");
};

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
document.body.addEventListener("click", buttonState);
