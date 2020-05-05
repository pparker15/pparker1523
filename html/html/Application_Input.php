
<?php
	$DB_SERVER = 'localhost:3306';
	$DB_USERNAME = 'parker';
	$DB_PASSWORD = 'password';
	$DB_DATABASE = 'user_profiling';
	
	$conn = mysqli_connect($DB_SERVER, $DB_USERNAME, $DB_PASSWORD, $DB_DATABASE);
?>

<!DOCTYPE HTML>
<html>
	<head>
		 <title>Applications</title>
	</head>

	<body>
		<table style="width:100%; border:1px solid black;">
			<tr>
				<th style="border:1px solid black;">Application_name</th>
				<th style="border:1px solid black;">Category</th>
				<th style="border:1px solid black;">Count time</th>
				<th style="border:1px solid black;">Number of flows</th>
			</tr>
			<?php
				$appSelect = mysqli_query($conn, "SELECT*FROM application_type;");
				if(mysqli_num_rows($appSelect) > 0){
					while($row = mysqli_fetch_array($appSelect)){
			?>
			<tr>
                        	<td style="border:1px solid black;"><?php echo $row["Application_name"]; ?></td>
                        	<td style="border:1px solid black;"><?php echo $row["Category"]; ?></td>
				<td style="border:1px solid black;"><?php echo $row["time_between_flows"]; ?></td>
				<td style="border:1px solid black;"><?php echo $row["no_required_flows"]; ?></td>

                    	</tr>
			<?php
					}
				}
				else{
					echo "No results found";
				}
			?>
		</table>
		</br>
		</br>

		<form method = "POST" action = "Application_Input.php" enctype="multipart/form-data">
			<input type = "text" name = "Application_name" placeholder = "Application Name" required>
			<br>
			<input type = "text" name = "Category" placeholder = "Category" required>
			<br>
			<input type = "text" name = "time_between_flows" placeholder = "Time between flows">
			<br>
			<input type = "number" name = "no_required_flows" placeholder = "Number Required flows">
			<br><br>
			<input type = "submit" name = "enter_app" value = "Add Application">
		</form>
	<?php
		if(isset($_POST["enter_app"])){
			$app_name = strip_tags(trim($_POST['Application_name']));
			$Category = strip_tags(trim($_POST['Category']));
			$time_between = strip_tags(trim($_POST['time_between_flows']));
			$no_required = strip_tags(trim($_POST['no_required_flows']));
			$app_name = mysqli_real_escape_string($conn, $app_name);
			$Category = mysqli_real_escape_string($conn, $Category);
			$time_between = mysqli_real_escape_string($conn, $time_between);
			$no_required = mysqli_real_escape_string($conn, $no_required);

			$sql = "INSERT INTO application_type (Application_name, Category, time_between_flows, no_required_flows) VALUES ('$app_name', '$Category', '$time_between', '$no_required');";
			mysqli_query($conn, $sql);
			echo "User created";
			echo "<meta http-equiv='refresh' content='0'>";
		} 

	?>
	
	

	
	</body>
<html>


