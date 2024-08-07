const validateJoinForm = () => {
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('password_confirm').value;
  const user_id = document.getElementById('user_id').value;
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

    if (user_id && nickname) {
      requestBtn.classList.remove('bg-Low');
      requestBtn.classList.add('bg-Primary');
    } else {
      requestBtn.classList.remove('bg-Primary');
      requestBtn.classList.add('bg-Low');
    }
  }
};

const validateLoginForm = () => {
  const user_id = document.getElementById('user_id').value;
  const password = document.getElementById('password').value;
  const requestBtn = document.getElementById('request_login_btn');

  if (user_id && password) {
    requestBtn.removeAttribute('disabled');
    requestBtn.classList.remove('bg-Low');
    requestBtn.classList.add('bg-Primary');
  } else {
    requestBtn.setAttribute('disabled', true);
    requestBtn.classList.remove('bg-Primary');
    requestBtn.classList.add('bg-Low');
  }
};

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
