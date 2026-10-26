(function () {
  const data = window.JUNOWED_DATA;
  const grid = document.querySelector("[data-template-grid]");
  const filters = document.querySelector("[data-template-filters]");
  const count = document.querySelector("[data-template-count]");
  let active = "all";

  function card(template) {
    return `<article class="template-card" style="--accent:${template.palette[1]}">
      <a class="template-cover" href="${template.preview}" aria-label="Xem mẫu ${template.title}">
        <img src="${template.cover}" alt="Mẫu thiệp ${template.title}" loading="lazy">
        <span class="preview-chip">Xem mẫu <b>↗</b></span>
      </a>
      <div class="template-copy">
        <div class="template-meta"><span>${template.style}</span><time>${template.date}</time></div>
        <h3>${template.title}</h3>
        <p>${template.couple}</p>
        <a class="text-link" href="${template.preview}">Mở bản thiệp <span>→</span></a>
      </div>
    </article>`;
  }

  function render() {
    const items = data.templates.filter(item => active === "all" || item.category === active);
    grid.innerHTML = items.map(card).join("");
    count.textContent = `${items.length} mẫu thiệp`;
  }

  filters.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-filter]");
    if (!button) return;
    active = button.dataset.filter;
    filters.querySelectorAll("button").forEach(btn => btn.classList.toggle("is-active", btn === button));
    render();
  });

  render();
})();
