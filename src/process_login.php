<?php

$login_error_messages = [
  "Login failed. Please try again.",
  "Login failed. Please try again",
  "An error with the database has occured, please try again.",
  "Invalid login credentials. Please verify that you are in the correct login page.",
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  // Sanitize input
  $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_STRING);
  $password = filter_input(INPUT_POST, 'password', FILTER_SANITIZE_STRING);

  $enteredstring = $username . $password;

  // Check for SQL injection attempts
  $sql_injection_words = array('insert', 'select', 'from', 'update', 'delete');
  foreach ($sql_injection_words as $word) {
    if (stripos($enteredstring, $word) !== false) {
      // Set 400 Bad Request status code and send error message
      http_response_code(401);
      $random_error_message = array_rand($login_error_messages);
      echo $login_error_messages[$random_error_message];
      exit();
    }
  }

  // Check for XSS attacks, specifically alert
  if (stripos($enteredstring, '<script>') !== false || 
      stripos($enteredstring, '</script>') !== false ||
      stripos($enteredstring, 'alert(') !== false) {
    // Set 400 Bad Request status code and send error message
    http_response_code(401);
    echo '<script>alert();</script>';
    exit();
  }

  // Check for XSS attacks, specifically prompt
  if (stripos($enteredstring, '<script>') !== false || 
      stripos($enteredstring, '</script>') !== false ||
      stripos($enteredstring, 'prompt(') !== false) {
    // Set 400 Bad Request status code and send error message
    http_response_code(401);
    echo '<script>prompt();</script>';
    exit();
  }

  http_response_code(401);
  echo "Login failed. Please try again.";
  exit();
}

?>