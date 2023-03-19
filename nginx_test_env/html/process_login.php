<?php 
    
    include "head.inc.php";
    include "nav.inc.php"; 
    $email = $errorMsg = ""; 
    $fname = "";
    $lname = "";
    $pwd = $_POST["pwd"];
    $pwd_hashed = "";
    $algo=PASSWORD_DEFAULT;
    $success = true; 
    
    if (empty($_POST["email"])) 
    { 
        $errorMsg .= "Email is required.<br>"; 
        $success = false; 
    } else 
    { 
        $email = sanitize_input($_POST["email"]); 
        
        // Additional check to make sure e-mail address is well-formed.     
        if (!filter_var($email, FILTER_VALIDATE_EMAIL))
        { 
            $errorMsg .= "Invalid email format."; 
            $success = false; 
        } 
    } 
    if ($success)
    {
        $pwd_hashed = password_hash($pwd, $algo);
        authenticateUser();
    }
    echo "<header class='register_process_header'> </header> <main class='container border-top register_process_main'> ";
        if ($success) 
        { 
            echo "<h3>Login successful!</h4>";     
            echo "<h4>Welcome back, " . $fname . " " . $lname . ".<br>"; 
            echo "<a class='btn btn-success register_process_btn' href='index.php'>Return to Home</a>";
        } else 
        { 
            echo "<h3>Oops!";
            echo "<h4>The following errors were detected:</h4>";     
            echo "<p>" . $errorMsg . "</p>"; 
            echo "<a class='btn btn-warning register_process_btn' href='login.php'>Return to Login</a>";
        } 
    echo "</main>";

    //Helper function that checks input for malicious or unwanted content. 
    function sanitize_input($data) 
    { 
        $data = trim($data); 
        $data = stripslashes($data);   
        $data = htmlspecialchars($data);   
        return $data; 
    }
    
    function authenticateUser() 
    { 
        global $fname, $lname, $email, $pwd_hashed, $errorMsg, $success;  
        // Create database connection. 
        $config = parse_ini_file('../../private/db-config.ini'); 
        $conn = new mysqli($config['servername'], $config['username'], $config['password'], $config['dbname']);  
        // Check connection     
        if ($conn->connect_error) 
        { 
            $errorMsg = "Connection failed: " . $conn->connect_error;         
            $success = false; 
        }     
        else 
        { 
            // Prepare the statement: 
            $stmt = $conn->prepare("SELECT * FROM world_of_pets_members WHERE email=?");
            // Bind & execute the query statement:         
            $stmt->bind_param("s", $email); 
            $stmt->execute(); 
            $result = $stmt->get_result();         
            if ($result->num_rows > 0) 
            { 
                // Note that email field is unique, so should only have 
                // one row in the result set. 
                $row = $result->fetch_assoc(); 
                $fname = $row["fname"];             
                $lname = $row["lname"]; 
                $pwd_hashed = $row["password"];
                // Check if the password matches:             
                if (!password_verify($_POST["pwd"], $pwd_hashed)) 
                { 
                    // Don't be too specific with the error message - hackers don't 
                    // need to know which one they got right or wrong. :) 
                    $errorMsg = "Email not found or password doesn't match..."; 
                    $success = false; 
                }
            }         
            else 
            { 
                $errorMsg = "Email not found or password doesn't match..."; 
                $success = false; 
            } 
            $stmt->close(); 
        }
        $conn->close(); 
    } 

    include "footer.inc.php"; 
?> 
