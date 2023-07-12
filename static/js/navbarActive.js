// const bar = document.getElementById("bar");
// const close = document.getElementById("close");
// const nav = document.getElementById("navbar");

// if (bar) {
//   bar.addEventListener("click", () => {
//     nav.classList.add("active");
//   });
// }
// if (close) {
//   close.addEventListener("click", () => {
//     nav.classList.remove("active");
//   });
// }

// console.log('Navbar js file ');


document.addEventListener('DOMContentLoaded', function() {
    var navbar = document.querySelector('#navbar');
  
    navbar.addEventListener('click', function(event) {
      if (event.target.tagName === 'A') {
        var currentActive = navbar.querySelector('.active');
  
        if (currentActive) {
          currentActive.classList.remove('active');
        }
  
        event.target.classList.add('active');
      }
    });
  });
  
  