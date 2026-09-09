(function () {
  "use strict";

  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");
  const navLinks = navMenu ? Array.from(navMenu.querySelectorAll(".nav-link")) : [];

  function setMenuOpen(isOpen) {
    if (!navToggle || !navMenu) return;
    navToggle.setAttribute("aria-expanded", String(isOpen));
    navMenu.classList.toggle("is-open", isOpen);
    navToggle.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
  }

  function closeMenu() {
    setMenuOpen(false);
  }

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", function () {
      const isOpen = navToggle.getAttribute("aria-expanded") === "true";
      setMenuOpen(!isOpen);
    });

    navLinks.forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && navToggle.getAttribute("aria-expanded") === "true") {
        closeMenu();
        navToggle.focus();
      }
    });

    document.addEventListener("click", function (event) {
      if (!navMenu.classList.contains("is-open")) return;
      const target = event.target;
      if (
        target instanceof Node &&
        !navMenu.contains(target) &&
        !navToggle.contains(target)
      ) {
        closeMenu();
      }
    });
  }
})();
