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

  if(isset($_POST['delete'])){
    $Result = mysqli_query($conn, "DELETE FROM Users WHERE User_IP_addr = '$oldIP';");
  }else{
    $Result2 = mysqli_query($conn, "UPDATE Users SET User_IP_addr ='$newIP', User_Name = '$newuname' WHERE User_IP_addr ='$oldIP';");
  }

?>
  <meta http-equiv="refresh" content="1; url=User_input.php"/>
</body>
</html>

