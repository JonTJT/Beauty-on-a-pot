<?php
$search_error_messages = [
  "No items found.",
  "No items found",
  "An error with the database has occured, please try again.",
  "Column empty.",
  "Row empty.",
];

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
  // Sanitize input
  $entered_string = filter_input(INPUT_GET, 'search', FILTER_SANITIZE_STRING);
  // Check for SQL injection attempts
  $sql_injection_words = array('insert', 'select', 'from', 'update', 'delete');
  foreach ($sql_injection_words as $word) {
    if (stripos($entered_string, $word) !== false) {
      // Set 401 error code
      http_response_code(401);
      $random_error_message = array_rand($search_error_messages);
      echo $search_error_messages[$random_error_message];
      exit();
    }
  }
  
    // Check for XSS attacks, specifically alert
    if (stripos($entered_string, '<script>') !== false || 
        stripos($entered_string, '</script>') !== false ||
        stripos($entered_string, 'alert(') !== false) {
      http_response_code(401);
      echo '<script>alert();</script>';
      exit();
    }
  
    // Check for XSS attacks, specifically prompt
    if (stripos($entered_string, '<script>') !== false || 
        stripos($entered_string, '</script>') !== false ||
        stripos($entered_string, 'prompt(') !== false) {
      http_response_code(401);
      echo '<script>prompt();</script>';
      exit();
    }

  http_response_code(401);
  echo "No items found.";
  exit();
}

?>