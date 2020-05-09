<?php
	$DB_SERVER = 'localhost:3306';
	$DB_USERNAME = 'parker';
	$DB_PASSWORD = 'password';
	$DB_DATABASE = 'user_profiling';
	
	$conn = mysqli_connect($DB_SERVER, $DB_USERNAME, $DB_PASSWORD, $DB_DATABASE);
?>

<!DOCTYPE html>
<html>
<head>
  <title></title>
</head>
<body>
<?php
  $oldIP = $_GET['oldIP'];
  $newIP = $_POST['upIPAddr'];
  $newuname = $_POST['uname'];
  #if(!preg_match("/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/", $newIP)){
  #    echo "Ensure IP address is entered";
  #}else{

  #}
  
  

  if(isset($_POST['delete'])){
    if(!mysqli_query($conn, "DELETE FROM Users WHERE User_IP_addr = '$oldIP';")){
	echo "There was an error. Please try again.";
    }else{
 	echo "<meta http-equiv='refresh' content='1; url=User_input.php'/>";
    }
  }else{
    if(!preg_match("/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/", $newIP)){
      echo "Ensure IP address is entered";
    }else{
	if(!mysqli_query($conn, "UPDATE Users SET User_IP_addr ='$newIP', User_Name = '$newuname' WHERE User_IP_addr ='$oldIP';")){
   	   echo "There was an error. Please try again.";
        }else{
 	   echo "<meta http-equiv='refresh' content='1; url=User_input.php'/>";
        }
    }
    
  }

?>
  
</body>
</html>

