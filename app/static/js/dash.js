// Dashboard
let mask = document.querySelector(".mask");
let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");
// let closeBtn2 = document.querySelector("#btn2");
let logoName = document.querySelector(".logo_name");
let logoDetails = document.querySelector(".logo-details");
closeBtn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  console.log(sidebar.classList);
  menuBtnChange();
});
// closeBtn2.addEventListener("click", ()=>{
//   sidebar.classList.toggle("open");
//   menuBtnChange();
// });
mask.addEventListener("click", () => {  sidebar.classList.toggle("open");   menuBtnChange(); });

searchBtn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  menuBtnChange();
});

function menuBtnChange() {
  if (sidebar.classList.contains("open")) {
    sidebar.style.display = "block";
    logoName.style.opacity = 1;
    logoDetails.style.background = "#e4e9f7";
    closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
  } else {
    if (window.innerWidth < 600) {
      sidebar.style.display = "none";
    }
    logoName.style.opacity = 0;
    logoDetails.style.background = "transparent";
    closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
  }
}

// change opacity
// let mapbtn = document.querySelector("#tab-map");
// let topMenu = document.querySelector(".top-menu");
// mapbtn.addEventListener("click",()=>{
//     topMenu.classList.toggle("top-menu");
//     opacityChange();
// });

// Dashboard nav sections

document.addEventListener("DOMContentLoaded", function () {
  function showSection() {
    var hash = window.location.hash.substring(1);
    var targetId = hash || "data";
    var targetSection = document.getElementById(targetId);
    if (targetSection) {
      var sections = document.querySelectorAll(".home-section");
      sections.forEach(function (section) {
        section.style.display = "none";
      });
      targetSection.style.display = "block";
    }
  }

  var navLinks = document.querySelectorAll('.nav-list a[href^="#"]');
  // var noDevice = document.querySelectorAll('.no-device a');

  navLinks.forEach(function (link) {
    link.addEventListener("click", function (event) {
      event.preventDefault();

      var sections = document.querySelectorAll(".home-section");
      sections.forEach(function (section) {
        section.style.display = "none";
      });

      var targetId = link.getAttribute("href").substring(1);
      var targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.style.display = "block";
        window.location.hash = targetId;
      }
    });
  });
  // var dataLink = document.getElementById('pills-data');
  // if(dataLink){
  //   dataLink.click();
  // }

  showSection();
});

// sendprofilepicture
function showImg() {
  var image = document.getElementById("profile");
  if (image.files.length > 0) {
    var file = image.files[0];
    var formData = new FormData();
    formData.append("profile", file);
    var userId = JSON.parse(document.getElementById("id").textContent);
    // console.log(formData);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/dashboard/" + userId + "/profile/upload", true);

    xhr.onload = function () {
      if (xhr.status === 201) {
        console.log("File uploaded successfully: ", xhr.responseText);
      } else {
        console.error("Error uploading file:", xhr.statusText);
      }
      location.reload();
    };
    xhr.onerror = function () {
      console.error("Network error occurred while uploading the file.");
    };

    xhr.send(formData);
  }
}
