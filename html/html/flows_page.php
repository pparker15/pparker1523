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
		<link rel="stylesheet" type="text/css" href="stylesheet.css">
	</head>

	<header>
		<ul>
			<li><a href='index.php'>Home Page</a></li>
      			<li><a href='flows_page.php'>Flows</a></li>
      			<li><a href='Application_Input.php'>Applications</a></li>
			<li><a href='User_input.php'>Users</a></li>
		</ul>
	</header>

	<body>	
	<h1>Users</h1>
		<div class = "column">
			<h2>View users</h2>
			<?php
				$userSelect = mysqli_query($conn, "SELECT*FROM Users;");
				if(mysqli_num_rows($userSelect) > 0){
					echo " <table>
						<tr>
						<th>IP Address</th>
						<th>Name</th>
						<th>Action</th>
						</tr>";
					while($row = mysqli_fetch_array($userSelect)){
						$oldIP = $row['User_IP_addr'];
						$olduname = $row['User_Name'];
						echo "<form method='POST' action='edituser.php?oldIP=$oldIP'>
						      <tr>
						      <td><input type='text' value ='{$oldIP}' name='upIPAddr'></td>
						      <td><input type='text' value='{$olduname}' name='uname'></td>
						      <td><input type='submit' value='Update' name='update'>
						      <input type='submit' value='Delete' name='delete'></td>
						      </tr>
						     </form>";
		    	
					}
				echo "</table>";
				}
				else{
					echo "No results found";
				}
			?>
				
			<h3> Create a user</h3>
			<div class="INSERT">
				<form method = "POST" action = "User_input.php" enctype="multipart/form-data">
					<label for="user_ip_address">IP Address</label>
					<input type = "text" name = "user_ip_address" placeholder = "IP Address" required>
					<br>
					<label for="name">Name</label>
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
			
			</div>
			
		</div>
	</body>
<html>
