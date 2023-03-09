<?php 
    
    include "head.inc.php";
    include "nav.inc.php"; 
    $email = $errorMsg = ""; 
    $fname = sanitize_input($_POST["fname"]);
    $lname = sanitize_input($_POST["lname"]);
    $pwd = $_POST["pwd"];
    $pwd_confirm = $_POST["pwd_confirm"];
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
    
    if ($pwd == $pwd_confirm){
        $pwd_hashed = password_hash($pwd, $algo);
    } else
    {
        $success = false;
        $errorMsg .= "<br>Passwords do not match.";
    }
    if ($success)
    {
        saveMemberToDB();
    }
    echo "<header class='register_process_header'> </header> <main class='container border-top register_process_main'> ";
        if ($success) 
        { 
            echo "<h3>Your registration is successful!</h4>";     
            echo "<h4>Thank you for signing up, " . $fname . " " . $lname . ".<br>"; 
            echo "<a class='btn btn-success register_process_btn' href='login.php'>Log-in</a>";
        } else 
        { 
            echo "<h3>Oops!";
            echo "<h4>The following errors were detected:</h4>";     
            echo "<p>" . $errorMsg . "</p>"; 
            echo "<a class='btn btn-danger register_process_btn' href='register.php'>Return to Sign Up</a>";
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
    /* 
 * Helper function to write the member data to the DB 
 */ 
    function saveMemberToDB() 
    { 
        global $fname, $lname, $email, $pwd_hashed, $errorMsg, $success;  
        // Create database connection. 
        $config = parse_ini_file('../../private/db-config.ini'); 
        $conn = new mysqli($config['servername'], $config['username'], $config['paszsword'], $config['dbname']);  
        // Check connection     
        if ($conn->connect_error) 
        { 
            $errorMsg = "Connection failed: " . $conn->connect_error;
            $success = false; 
        }     
        else 
        { 
            // Prepare the statement: 
            $stmt = $conn->prepare("INSERT INTO world_of_pets_members (fname, lname, email, password) VALUES (?, ?, ?, ?)"); 

            // Bind & execute the query statement: 
            $stmt->bind_param("ssss", $fname, $lname, $email, $pwd_hashed);
            if (!$stmt->execute()) 
            { 
                $errorMsg = "Execute failed: (" . $stmt->errno . ") " . $stmt->error; 
                $success = false; 
            } 
            $stmt->close(); 
        } 
        $conn->close(); 
    } 

        include "footer.inc.php"; 
?> 
