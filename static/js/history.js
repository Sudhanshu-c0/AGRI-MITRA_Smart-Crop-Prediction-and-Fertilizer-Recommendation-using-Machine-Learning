/**
 * History Table Client-side Search and Filter
 */
document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('historySearch');
  const table = document.querySelector('.table tbody');

  if (searchInput && table) {
    searchInput.addEventListener('input', function () {
      const q = searchInput.value.toLowerCase();
      const rows = table.querySelectorAll('tr');
      rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(q) ? '' : 'none';
      });
    });
  }
});
