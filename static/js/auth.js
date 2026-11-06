/**
 * Auth Scripts - Password Matching and Confirmation
 */
document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const pwd = document.querySelector('input[name="password"]');
  const confirmPwd = document.querySelector('input[name="confirm_password"]');

  if (form && pwd && confirmPwd) {
    form.addEventListener('submit', function (e) {
      if (pwd.value !== confirmPwd.value) {
        e.preventDefault();
        alert('Passwords do not match. Please verify.');
        confirmPwd.focus();
      }
    });
  }
});
