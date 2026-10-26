const toast = document.querySelector('#toast');
const weddings = [
  ['MA', 'Minh Anh & Tuấn Kiệt', 'minhanh-tuankiet.hysu.vn', 'Mộc Lan', 'Đã xuất bản', '48 / 120', '12 phút trước', 'a1'],
  ['HN', 'Hoàng Nam & Bảo Trân', 'hoangnam-baotran.hysu.vn', 'Giao Mùa', 'Đã xuất bản', '31 / 80', '38 phút trước', 'a2'],
  ['TL', 'Thảo Linh & Đức Minh', 'Chưa có tên miền', 'Thanh Xuân', 'Bản nháp', '—', '2 giờ trước', 'a3']
];
const notify = (message) => { toast.textContent = message; toast.classList.add('show'); clearTimeout(notify.timer); notify.timer = setTimeout(() => toast.classList.remove('show'), 2800); };
const badge = (status) => `<span class="badge ${status === 'Đã xuất bản' || status === 'Đã thanh toán' ? 'live' : 'draft'}">● ${status}</span>`;
function renderRows(rows = weddings) {
  return rows.map((item) => `<tr><td><div class="couple"><div class="couple-ava ${item[7]}">${item[0]}</div><div><strong>${item[1]}</strong><small>${item[2]}</small></div></div></td><td>${item[3]}</td><td>${badge(item[4])}</td><td><strong>${item[5].split(' / ')[0]}</strong>${item[5].includes('/') ? ` <small>/ ${item[5].split(' / ')[1]}</small>` : ''}</td><td>${item[6]}</td><td><button class="more edit-wedding" data-index="${weddings.indexOf(item)}">•••</button></td></tr>`).join('') || '<tr><td colspan="6" class="empty">Không tìm thấy thiệp cưới phù hợp.</td></tr>';
}
function bindRowActions() { document.querySelectorAll('.edit-wedding').forEach(button => button.addEventListener('click', () => openEditor(Number(button.dataset.index)))); }
function updateTables() { document.querySelectorAll('.wedding-rows').forEach(body => body.innerHTML = renderRows()); bindRowActions(); document.querySelector('#wedding-count').textContent = weddings.length; }
function showPage(id) {
  document.querySelectorAll('.page-view').forEach(page => page.hidden = page.id !== `page-${id}`);
  document.querySelectorAll('.nav-link').forEach(link => link.classList.toggle('active', link.getAttribute('href') === `#${id}`));
  const link = document.querySelector(`.nav-link[href="#${id}"]`);
  document.querySelector('#page-title').textContent = link.dataset.page;
  document.querySelector('#page-subtitle').textContent = link.dataset.subtitle;
  document.querySelector('.sidebar').classList.remove('open');
}
function openModal() { document.querySelector('#wedding-modal').classList.add('open'); document.body.classList.add('modal-open'); }
function closeModal() { document.querySelector('#wedding-modal').classList.remove('open'); document.body.classList.remove('modal-open'); }
function openEditor(index) { const item = weddings[index]; const form = document.querySelector('#wedding-form'); form.dataset.index = index; document.querySelector('#modal-title').textContent = 'Chỉnh sửa thiệp cưới'; document.querySelector('#couple-name').value = item[1]; document.querySelector('#template-name').value = item[3]; document.querySelector('#domain-name').value = item[2] === 'Chưa có tên miền' ? '' : item[2].replace('.hysu.vn', ''); document.querySelector('#publish-status').value = item[4]; document.querySelector('#delete-wedding').hidden = false; openModal(); }
function openCreate() { const form = document.querySelector('#wedding-form'); form.reset(); delete form.dataset.index; document.querySelector('#modal-title').textContent = 'Tạo thiệp cưới mới'; document.querySelector('#delete-wedding').hidden = true; openModal(); }
document.querySelectorAll('.nav-link').forEach(link => link.addEventListener('click', event => { event.preventDefault(); showPage(link.getAttribute('href').slice(1)); }));
document.querySelector('#new-wedding').addEventListener('click', openCreate);
document.querySelector('#hero-create').addEventListener('click', openCreate);
document.querySelector('#mobile-menu').addEventListener('click', () => document.querySelector('.sidebar').classList.toggle('open'));
document.querySelector('#search-button').addEventListener('click', () => document.querySelector('#global-search').focus());
document.querySelector('#global-search').addEventListener('input', event => { const query = event.target.value.toLowerCase(); document.querySelectorAll('.wedding-rows').forEach(body => body.innerHTML = renderRows(weddings.filter(item => item.join(' ').toLowerCase().includes(query)))); bindRowActions(); });
document.querySelector('#notification-button').addEventListener('click', () => document.querySelector('#notifications').classList.toggle('open'));
document.querySelector('#view-weddings').addEventListener('click', () => showPage('weddings'));
document.querySelector('.close-modal').addEventListener('click', closeModal);
document.querySelector('#wedding-modal').addEventListener('click', event => { if (event.target.id === 'wedding-modal') closeModal(); });
document.querySelector('#wedding-form').addEventListener('submit', event => { event.preventDefault(); const form = event.currentTarget, couple = document.querySelector('#couple-name').value.trim(), names = couple.split(/\s*&\s*/); const record = [names.map(name => name[0]).join('').slice(0, 2).toUpperCase(), couple, document.querySelector('#domain-name').value.trim() ? `${document.querySelector('#domain-name').value.trim().replace('.hysu.vn', '')}.hysu.vn` : 'Chưa có tên miền', document.querySelector('#template-name').value, document.querySelector('#publish-status').value, '0 / 100', 'Vừa xong', 'a1']; if (form.dataset.index !== undefined) weddings[form.dataset.index] = record; else weddings.unshift(record); updateTables(); closeModal(); notify(form.dataset.index !== undefined ? 'Đã lưu thay đổi.' : 'Đã tạo thiệp cưới mới.'); });
document.querySelector('#delete-wedding').addEventListener('click', () => { weddings.splice(Number(document.querySelector('#wedding-form').dataset.index), 1); updateTables(); closeModal(); notify('Đã xoá thiệp cưới.'); });
document.querySelectorAll('.template-card').forEach(card => card.addEventListener('click', () => { document.querySelectorAll('.template-card').forEach(item => item.classList.remove('selected')); card.classList.add('selected'); notify(`Đã chọn mẫu ${card.dataset.template}.`); }));
updateTables();
