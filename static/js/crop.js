/**
 * Crop Form Validation & Real-time Feedback
 */
document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('#cropPredictionForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span>🌱 Analyzing Soil & Climate...</span>';
    }
  });
});
