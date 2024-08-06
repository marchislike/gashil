function validateJoinForm() {
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('password_confirm').value;
  const username = document.getElementById('username').value;
  const nickname = document.getElementById('nickname').value;
  const warningText = document.getElementById('password_error');
  const requestBtn = document.getElementById('request_join_btn');

  if (password !== confirmPassword) {
    warningText.style.display = 'block';
    requestBtn.setAttribute('disabled', true);
    requestBtn.classList.remove('bg-Primary');
    requestBtn.classList.add('bg-Low');
  } else {
    warningText.style.display = 'none';
    requestBtn.removeAttribute('disabled');

    if (username && nickname) {
      requestBtn.classList.remove('bg-Low');
      requestBtn.classList.add('bg-Primary');
    } else {
      requestBtn.classList.remove('bg-Primary');
      requestBtn.classList.add('bg-Low');
    }
  }
}

function validateLoginForm() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const requestBtn = document.getElementById('request_login_btn');

  if (username && password) {
    requestBtn.removeAttribute('disabled');
    requestBtn.classList.remove('bg-Low');
    requestBtn.classList.add('bg-Primary');
  } else {
    requestBtn.setAttribute('disabled', true);
    requestBtn.classList.remove('bg-Primary');
    requestBtn.classList.add('bg-Low');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document
    .getElementById('join_form')
    .addEventListener('input', validateJoinForm);
});

document.addEventListener('DOMContentLoaded', () => {
  document
    .getElementById('login_form')
    .addEventListener('input', validateLoginForm);
});
