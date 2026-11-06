/**
 * Profile Edit & Password Change Scripts
 */
document.addEventListener('DOMContentLoaded', function () {
  const pwdForm = document.querySelector('#changePwdForm');
  if (pwdForm) {
    pwdForm.addEventListener('submit', function (e) {
      const newPwd = document.getElementById('new_password').value;
      const confPwd = document.getElementById('confirm_password').value;
      if (newPwd !== confPwd) {
        e.preventDefault();
        alert('New passwords do not match!');
      }
    });
  }
});
