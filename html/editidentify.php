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
  			$appID = $_GET['appID'];
  			$identify = $_GET['identify'];
  			$newAppID = $_POST['appID'];
  			$newidentify_by = $_POST['new_Identify_By'];
			# Delete record
  			if(isset($_POST['delete'])){
    				if(!mysqli_query($conn, "DELETE FROM Identify_apps WHERE App_ID = '$appID' AND identify_by = '$identify';")){
					echo "There was an error. Please try again.";
    				}else{
					echo "<meta http-equiv='refresh' content='1; url=Application_Input.php'/>";
    				}
			# Update record
  			}else{
    				if(!mysqli_query($conn, "UPDATE Identify_apps SET App_ID ='$newAppID', identify_by = '$newidentify_by' WHERE App_ID = '$appID' AND identify_by = '$identify';")){
					echo "There was an error";
    				}else{
					echo "<meta http-equiv='refresh' content='1; url=Application_Input.php'/>";
    				}
  			}

		?>
  
	</body>
</html>
