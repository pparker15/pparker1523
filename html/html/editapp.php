<?php
	# Database connection
	$DB_SERVER = 'localhost:3306';
	$DB_USERNAME = 'parker';
	$DB_PASSWORD = 'password';
	$DB_DATABASE = 'application_identification';
	
	$conn = mysqli_connect($DB_SERVER, $DB_USERNAME, $DB_PASSWORD, $DB_DATABASE);
?>

<!DOCTYPE html>
<html>
	<head>
  		<title></title>
	</head>
	<body>

		<?php
  			$App_ID = $_GET['appID'];
  			$App_name = $_POST['newAppName'];
  			$Category = $_POST['newCategory'];
 			$time = $_POST['newTime'];
  			$number_flows = $_POST['newNumber'];

  			if(isset($_POST['delete'])){
			# Delete application from the database.
				if(!mysqli_query($conn, "DELETE FROM application_type WHERE App_ID = '$App_ID';")){
					echo "There was an error. Ensure identify by records associated with this App ID is deleted first";
				}else{
					echo "App deleted";
					echo "<meta http-equiv='refresh' content='1; url=Application_Input.php'/>";
				}
			# Update the application in the database.
  			}else{
	
			  	if(empty($time) and empty($number_flows)){
					$sql = "UPDATE application_type SET Application_name = '$App_name', Category = '$Category', time_between_flows = null, no_required_flows = null WHERE App_ID = '$App_ID';";
				}
				elseif(empty($time)){
					$sql = "UPDATE application_type SET Application_name = '$App_name', Category = '$Category', time_between_flows = null, no_required_flows = $number_flows WHERE App_ID = '$App_ID';";
				}elseif(empty($number_flows)){
					$sql = "UPDATE application_type SET Application_name = '$App_name', Category = '$Category', time_between_flows = '$time', no_required_flows = null  WHERE App_ID = '$App_ID';";
				}else{
					$sql = "UPDATE application_type SET Application_name = '$App_name', Category = '$Category', time_between_flows = '$time', no_required_flows = $number_flows WHERE App_ID = '$App_ID';";
				}
				if(!mysqli_query($conn, $sql)){
					echo "There was an error please try again";	
				}else{
					echo "App updated";
					echo "<meta http-equiv='refresh' content='1; url=Application_Input.php'/>";
				}
				
			}
		?>
  
	</body>
</html>
