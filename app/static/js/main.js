document.addEventListener("DOMContentLoaded", () => {
  // Password Validation
  const pwd = document.querySelector('input[name="password"]');
  if (pwd) {
    pwd.addEventListener("input", () => {
      const msg = document.querySelector("#passwordHelp");
      if (!msg) return;

      const v = pwd.value;
      const strong =
        v.length >= 8 &&
        /[A-Z]/.test(v) &&
        /[a-z]/.test(v) &&
        /[0-9]/.test(v) &&
        /[!@#$%^&*(),.?\"\':;{}|<>\/\\\-_+=]/.test(v);

      msg.textContent = strong
        ? "Strong password ✅"
        : "Use at least 8 chars, with upper, lower, number, and special symbol.";
      msg.className = strong
        ? "form-text text-success"
        : "form-text text-danger";
    });
  }

  const themeToggle = document.getElementById("theme-toggle");
  const icon = themeToggle?.querySelector("i");
  const html = document.documentElement;
  const navbar = document.querySelector(".navbar");

  let currentTheme = localStorage.getItem("theme") || "dark";

  const applyTheme = (theme) => {
    html.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);

    if (icon) {
      icon.className = theme === "dark" ? "fas fa-sun" : "fas fa-moon";
    }

    if (navbar) {
      if (theme === "light") {
        navbar.classList.remove("navbar-dark");
        navbar.classList.add("navbar-light");
      } else {
        navbar.classList.remove("navbar-light");
        navbar.classList.add("navbar-dark");
      }
    }
  };

  // Apply initial theme
  applyTheme(currentTheme);

  // Event Listener
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      currentTheme = currentTheme === "dark" ? "light" : "dark";
      applyTheme(currentTheme);
    });
  }
});
