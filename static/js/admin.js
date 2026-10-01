/**
 * Admin Dashboard 7-Day Chart & Analytics Scripts
 */

document.addEventListener('DOMContentLoaded', function () {
  const canvas = document.getElementById('analyticsChart');
  if (!canvas) return;

  const labels = JSON.parse(canvas.getAttribute('data-labels') || '[]');
  const cropCounts = JSON.parse(canvas.getAttribute('data-crops') || '[]');
  const fertCounts = JSON.parse(canvas.getAttribute('data-ferts') || '[]');

  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const width = canvas.parentElement.clientWidth;
  const height = 280;

  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = width + 'px';
  canvas.style.height = height + 'px';
  ctx.scale(dpr, dpr);

  const padding = { top: 30, right: 30, bottom: 40, left: 40 };
  const chartW = width - padding.left - padding.right;
  const chartH = height - padding.top - padding.bottom;

  const maxVal = Math.max(5, ...cropCounts, ...fertCounts);

  // Background Grid Lines
  ctx.strokeStyle = '#e5e7eb';
  ctx.lineWidth = 1;
  ctx.fillStyle = '#9ca3af';
  ctx.font = '11px sans-serif';
  ctx.textAlign = 'right';

  const gridSteps = 4;
  for (let i = 0; i <= gridSteps; i++) {
    const y = padding.top + (chartH / gridSteps) * i;
    const val = Math.round(maxVal - (maxVal / gridSteps) * i);
    ctx.beginPath();
    ctx.moveTo(padding.left, y);
    ctx.lineTo(width - padding.right, y);
    ctx.stroke();
    ctx.fillText(val, padding.left - 8, y + 4);
  }

  // Draw Line
  function drawLine(data, color, dotColor) {
    if (data.length === 0) return;
    const stepX = chartW / (data.length - 1 || 1);

    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.beginPath();

    data.forEach((val, idx) => {
      const x = padding.left + idx * stepX;
      const y = padding.top + chartH - (val / maxVal) * chartH;
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Dots
    ctx.fillStyle = dotColor;
    data.forEach((val, idx) => {
      const x = padding.left + idx * stepX;
      const y = padding.top + chartH - (val / maxVal) * chartH;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  // Draw Crops line (Emerald) and Fert line (Sky Blue)
  drawLine(cropCounts, '#2d6a4f', '#52b788');
  drawLine(fertCounts, '#0284c7', '#38bdf8');

  // X Axis Labels
  ctx.fillStyle = '#6b7280';
  ctx.textAlign = 'center';
  const stepX = chartW / (labels.length - 1 || 1);
  labels.forEach((lbl, idx) => {
    const x = padding.left + idx * stepX;
    ctx.fillText(lbl, x, height - 12);
  });
});
