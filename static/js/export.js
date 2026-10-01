/**
 * Export Feedback Utility
 */
document.addEventListener('DOMContentLoaded', function () {
  const exportLinks = document.querySelectorAll('a[href*="/export/"]');
  exportLinks.forEach(link => {
    link.addEventListener('click', function () {
      console.log('Downloading export dataset...');
    });
  });
});
