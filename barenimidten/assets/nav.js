/* Mobil-navigation: vis/skjul menu */
(function(){
  var btn = document.querySelector(".navtoggle");
  var nav = document.querySelector("nav.main");
  if(btn && nav){
    btn.addEventListener("click", function(){
      nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", nav.classList.contains("open"));
    });
  }
})();
