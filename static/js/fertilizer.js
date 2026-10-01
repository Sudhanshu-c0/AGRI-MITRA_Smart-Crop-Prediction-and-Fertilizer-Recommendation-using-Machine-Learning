/**
 * Fertilizer Form Client Scripts
 */
document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('#fertilizerForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span>🧪 Computing Optimal Formula...</span>';
    }
  });
});
