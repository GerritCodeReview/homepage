(function () {
  document.addEventListener("DOMContentLoaded", function () {
    var root = document.querySelector(".layout-page .post-content");
    if (!root) return;

    var headings = root.querySelectorAll("h2[id], h3[id], h4[id], h5[id]");
    headings.forEach(function (heading) {
      if (heading.querySelector(".heading-anchor")) return;

      var anchor = document.createElement("a");
      anchor.className = "heading-anchor";
      anchor.href = "#" + heading.id;
      anchor.setAttribute(
        "aria-label",
        "Link to section: " + heading.textContent.trim()
      );
      anchor.innerHTML = '<i class="fa-solid fa-link" aria-hidden="true"></i>';
      heading.appendChild(anchor);
    });
  });
})();
