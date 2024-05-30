<?php
$hostname = '******';
$username = '*****';
$password = '******';
$database = '*****';

$logFile = 'get_log.txt'; // Path to the log file

// Connect to the MySQL database
$mysqli = new mysqli($hostname, $username, $password, $database);

// Check connection
if ($mysqli->connect_error) {
    die("Connection failed: " . $mysqli->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    
    // Log the GET parameters
    $logData = date('Y-m-d H:i:s') . " - " . json_encode($_GET) . PHP_EOL;
    file_put_contents($logFile, $logData, FILE_APPEND | LOCK_EX);
    
    // Assuming the data is passed through query parameters
    $id = $_GET['id'];
    $app_address = $_GET['app_address'];
    $app_msgid = $_GET['app_msgid'];
    echo $app_msgid;
	echo '<br>';
    // Convert ISO 8601 formatted datetime to MySQL format
    $creation_date = date('Y-m-d H:i:s', strtotime($_GET['creation_date']));
    
    $mccmnc = $_GET['mccmnc'];
    $ope_address = $_GET['ope_address'];
    $ope_channel = $_GET['ope_channel'];
    $previd = $_GET['previd'];
	echo $previd;
	echo '<br>';
    $srstatus = $_GET['srstatus'];
    $text = $_GET['text'];
    $type = $_GET['type'];
    $tag = $_GET['tag'];

    // Check if srstatus is 2000
        if ($srstatus == 2000) {
        // Update table traitementsms using prepared statement
        $sql = "UPDATE traitementsms SET AC_sms = 'Delivered', IDA_sms = ? WHERE ID_sms = ?";
        $stmt = $mysqli->prepare($sql);
        
        // Bind parameters
        $stmt->bind_param("ss", $previd, $app_msgid);
        
        if ($stmt->execute()) {
            echo "Record updated successfully";
        } else {
            echo "Error updating record: " . $mysqli->error;
        }
        
        // Close statement
        $stmt->close();
    } else {
        
        $to = "relkarne@astus.fr"; 
        $subject = "Message $app_msgid";
        $message = "Le message envoyé à $ope_address dont l'ID est $app_msgid n'a pas été envoyé : $text";

        
        if (mail($to, $subject, $message)) {
            echo "Email sent successfully";
        } else {
            echo "Failed to send email";
        }
    }
}

?>
