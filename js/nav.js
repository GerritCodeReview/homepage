(function () {
  document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector(".site-header");
    if (!header) return;

    var navToggle = header.querySelector(".nav-toggle");
    var dropdowns = header.querySelectorAll(".site-nav .dropdown");

    function setDropdown(item, open) {
      item.classList.toggle("open", open);
      item.querySelector(".dropdown-toggle").setAttribute("aria-expanded", open);
    }

    function closeDropdowns(except) {
      dropdowns.forEach(function (item) {
        if (item !== except) setDropdown(item, false);
      });
    }

    if (navToggle) {
      navToggle.addEventListener("click", function () {
        var open = header.classList.toggle("nav-open");
        navToggle.setAttribute("aria-expanded", open);
      });
    }

    dropdowns.forEach(function (item) {
      item.querySelector(".dropdown-toggle").addEventListener("click", function () {
        closeDropdowns(item);
        setDropdown(item, !item.classList.contains("open"));
      });
    });

    document.addEventListener("click", function (event) {
      if (!header.contains(event.target)) closeDropdowns(null);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeDropdowns(null);
    });
  });
})();
