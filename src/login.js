const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const username = event.target.elements.username.value;
  const password = event.target.elements.password.value;

  // Make AJAX request to login.php
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'process_login.php');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Successful login
      const successMessage = document.querySelector('#error-message');
      successMessage.textContent = xhr.responseText;
      window.location.href = "admin/home.html";
    } else {
      // Login failed, display error message
      const errorMessage = document.querySelector('#error-message');
      if (xhr.status === 401) {
        errorMessage.textContent = xhr.responseText;
      } else {
        errorMessage.textContent = "An error occurred. Please try again later.";
      }
    }
  };
  const data = `username=${username}&password=${password}`;
  xhr.send(data);
});
