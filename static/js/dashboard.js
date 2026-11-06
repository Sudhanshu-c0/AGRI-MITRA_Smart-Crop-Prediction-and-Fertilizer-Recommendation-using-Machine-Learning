/**
 * User Dashboard Scripts
 */
document.addEventListener('DOMContentLoaded', function () {
  // Animated Counter for Metrics
  const counters = document.querySelectorAll('.stat-info h3');
  counters.forEach(counter => {
    const target = parseInt(counter.innerText, 10);
    if (isNaN(target) || target <= 0) return;
    let count = 0;
    const speed = Math.max(10, Math.floor(1000 / target));
    const timer = setInterval(() => {
      count++;
      counter.innerText = count;
      if (count >= target) clearInterval(timer);
    }, speed);
  });
});
