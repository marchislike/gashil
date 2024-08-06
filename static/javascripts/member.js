function checkMatchingPassword() {
  let password = document.getElementById('password').value;
  let confirmPassword = document.getElementById('password_confirm').value;
  let warningText = document.getElementById('password_error');
  if (password !== confirmPassword) {
    warningText.style.display = 'block';
  } else {
    warningText.style.display = 'none';
  }
}

document.addEventListener('DOMContentLoaded', () =>
  document
    .getElementById('joinForm')
    .addEventListener('input', checkMatchingPassword)
);
