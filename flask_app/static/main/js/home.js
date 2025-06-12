// Redirects to appropriate account creation template or login template based on button click
const login = function login() {
  window.location.href = '/login';
}

const account_creation = function account_creation() {
  window.location.href = '/create-account';
}

const sign_in_button = document.getElementById('sign-in');
sign_in_button.addEventListener('click', login);

const account_creation_button = document.getElementById('create-account');
account_creation_button.addEventListener('click', account_creation);