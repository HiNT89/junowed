(function () {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("template") || "classic-rose";
  const item = window.JUNOWED_DATA?.templates?.find(template => template.id === id);
  if (!item) return;
  document.title = `${item.couple} - Junowed`;
  const replacements = [
    [/Tiến Đạt/g, item.groom],
    [/Thanh Hằng/g, item.bride],
    [/29-03-2026/g, item.eventDateDisplay],
    [/29\/03\/2026/g, item.eventDateDisplay.replaceAll("-", "/")]
  ];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const textNodes = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode);
  textNodes.forEach(node => {
    if (["SCRIPT", "STYLE"].includes(node.parentElement?.tagName)) return;
    replacements.forEach(([from, to]) => { node.nodeValue = node.nodeValue.replace(from, to); });
  });
  document.querySelectorAll(".couple-name").forEach(node => {
    if (node.tagName !== "SPAN") node.innerHTML = item.couple.replace(" & ", " <span class=\"heart\">♥</span> ");
  });
  document.querySelectorAll("#clock").forEach(node => node.dataset.date = item.eventDate);
  document.querySelectorAll(".day_area_inner").forEach(node => {
    const [year, month, day] = item.eventDate.split("-");
    node.innerHTML = `${day}<img src="./images/common/heart-icon.png" alt="">${month}`;
  });
  const mainImage = document.querySelector(".main_image_area img");
  if (mainImage) mainImage.src = item.cover;
  if (window.config) {
    window.config.bgMusic = item.music;
    window.config.effect = { type: item.effect };
  }
})();
