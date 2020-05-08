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
  $App_ID = $_GET['appID'];
  $App_name = $_POST['newAppName'];
  $Category = $_POST['newCategory'];
  $time = $_POST['newTime'];
  $number_flows = $_POST['newNumber'];
  if(isset($_POST['delete'])){
    $Result = mysqli_query($conn, "DELETE FROM application_type WHERE App_ID = '$App_ID';");
  }else{
	
  }if(empty($time) and empty($number_flows)){
		$Result2 = mysqli_query($conn, "UPDATE application_type SET Application_name = '$App_name', Category = '$Category', time_between_flows = null, no_required_flows = null WHERE App_ID = '$App_ID';");
	}
	elseif(empty($time)){
		$Result2 = mysqli_query($conn, "UPDATE application_type SET Application_name = '$App_name', Category = '$Category', time_between_flows = null, no_required_flows = $number_flows WHERE App_ID = '$App_ID';");
	}elseif(empty($number_flows)){
		$Result2 = mysqli_query($conn, "UPDATE application_type SET Application_name = '$App_name', Category = '$Category', time_between_flows, no_required_flows = null = '$time' WHERE App_ID = '$App_ID';");
	}else{
		$Result2 = mysqli_query($conn, "UPDATE application_type SET Application_name = '$App_name', Category = '$Category', time_between_flows = '$time', no_required_flows = $number_flows WHERE App_ID = '$App_ID';");
	}
?>
  <meta http-equiv="refresh" content="1; url=Application_Input.php"/>
</body>
</html>


