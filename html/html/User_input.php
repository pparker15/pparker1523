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
		 <title>User's</title>
	</head>

	<body>
		<table style="width:100%; border:1px solid black;"">
			<tr>
				<th style="border:1px solid black;">User IP address</th>
				<th style="border:1px solid black;">User</th>
			</tr>
			<?php
				$userSelect = mysqli_query($conn, "SELECT*FROM Users;");
				if(mysqli_num_rows($userSelect) > 0){
					while($row = mysqli_fetch_array($userSelect)){
			?>
			<tr>
                        	<td style="border:1px solid black;"><?php echo $row["User_IP_addr"]; ?></td>
                        	<td style="border:1px solid black;"><?php echo $row["User_Name"]; ?></td>
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


		<form method = "POST" action = "User_input.php" enctype="multipart/form-data">
			<input type = "text" name = "user_ip_address" placeholder = "IP Address" required>
			<br>
			<input type = "text" name = "name" placeholder = "Name" required>
			<br><br>
			<input type = "submit" name = "enter_user" value = "Create User">
		</form>
	<?php
		if(isset($_POST["enter_user"])){
			$user_IP = strip_tags(trim($_POST['user_ip_address']));
			$name = strip_tags(trim($_POST['name']));
			$user_IP = mysqli_real_escape_string($conn, $user_IP);
			$name = mysqli_real_escape_string($conn, $name);

			$sql = "INSERT INTO Users (User_IP_Addr, User_Name) VALUES ('$user_IP', '$name');";
			mysqli_query($conn, $sql);
			echo "User created";
			echo "<meta http-equiv='refresh' content='0'>";
		} 

	?>
	
	

	
	</body>
<html>
