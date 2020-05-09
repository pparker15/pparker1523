
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
		<h1>Applications</h1>
		<h2>Important Information</h1>
		<p>Use the name table at the bottom of the page to learn about the applications that can be identified. To be able to recognise applications in flow, insert a new application name into the applications table. Then insert ways of identifying this application in the identify apps table by adding text from the name table. The flows table is not affected after changing information on this page.</p>

			

		<div class="both">
			<div class = "column left">
				<h2>How to identify applications</h2>
				<?php
				# Identify by display and input
					#Identify_apps, App_ID, identify_by;
					$appSelect = mysqli_query($conn, "SELECT*FROM Identify_apps;");
						
						if(mysqli_num_rows($appSelect) > 0){
							echo " <table>
							<tr>
							<th>Application ID</th>
							<th>Identify BY</th>
							<th>Action</th>
							</tr>";
							while($row = mysqli_fetch_array($appSelect)){
							$ID_App = $row['App_ID'];
							$identify_by = $row['identify_by'];
							echo "<form method='POST' action='editidentify.php?appID=$ID_App&identify=$identify_by'>
							      <tr>
							      <td><input type='text' value ='{$ID_App}' name='appID'></td>
							      <td><input type='text' value='{$identify_by}' name='new_Identify_By'></td>"
				?>
							      <td><input type='submit' value='Update' name='update' onclick="return confirm('Are you sure you want to update record?');">
							      <input type='submit' value='Delete' name='delete' onclick="return confirm('Are you sure you want to delete record?');"></td>
							      </tr>
							     </form>
				<?php
			    				
							}
							echo "</table>";
					}
					else{
						echo "No results found";
					}
				?>

				<h3>Add new way to identify applications<h3>
				<div class="INSERT">
					<form method = "POST" action = "Application_Input.php" enctype="multipart/form-data">
						<label for="AppID">Application ID</label>	
						<input type = "number" name = "AppID" placeholder = "Application ID" required>
						<br>
						<label for="identifier">Identifer</label>
						<input type = "text" name = "identifier" placeholder = "Identifier" required>
						<br><br>
						<input type = "submit" name = "enter_identifier" value = "Add Identifier">
					</form>
				</div>
				<?php
					if(isset($_POST["enter_identifier"])){
						$appID = strip_tags(trim($_POST['AppID']));
						$identifier = strip_tags(trim($_POST['identifier']));
						$appID = mysqli_real_escape_string($conn, $appID);
						$identifier = mysqli_real_escape_string($conn, $identifier);

						$sql1 = "INSERT INTO Identify_apps (App_ID, identify_by) VALUES ('$appID', '$identifier');";

						if(!mysqli_query($conn, $sql1)){
							echo "There was an error. Please ensure the ID is in the application table";
						}else{
							echo "Identifier added";
							echo "<meta http-equiv='refresh' content='0'>";
						}
					} 

				?>
			</div>

			<div class = "column right">
				<h2>Application types</h2>


				<?php
				# Display and input application types
					$appSelect = mysqli_query($conn, "SELECT*FROM application_type;");
						if(mysqli_num_rows($appSelect) > 0){
							echo " <table>
							<tr>
							<th>Application ID</th>
							<th>Application Name</th>
							<th>Category</th>
							<th>Time between flows</th>
							<th>Number of flows</th>
							<th>Action</th>
							</tr>";
							while($row = mysqli_fetch_array($appSelect)){
							$App_ID = $row['App_ID'];
							$App_name = $row['Application_name'];
							$Category = $row['Category'];
							$time = $row['time_between_flows'];
							$number_flows = $row['no_required_flows'];
							echo "<form method='POST' action='editapp.php?appID=$App_ID'></tr>
							      <tr>
							      <td><input type='text' value = '{$App_ID}' name = 'IDapp' readonly></td>
							      <td><input type='text' value ='{$App_name}' name='newAppName'></td>
							      <td><input type='text' value='{$Category}' name='newCategory'></td>
							      <td><input type='text' value='{$time}' name='newTime'></td>
							      <td><input type='number' value='{$number_flows}' name='newNumber'></td>"
				?>
							      <td><input type='submit' value='Update' name='update' onclick="return confirm('Are you sure you want to update the record?');">
							      <input type='submit' value='Delete' name='delete' onclick="return confirm('Are you sure you want to delete the record?');"></td>
							     </tr>
							     </form>
				<?php
			    	
						}
						echo "</table>";
					}
					else{
						echo "No results found";
					}
				?>

			
				<h3>Add an application</h3>
				<div class="INSERT">
					<form method = "POST" action = "Application_Input.php" enctype="multipart/form-data">
							
						<label for="Application_name">Application Name</label>	
						<input type = "text" name = "Application_name" placeholder = "Application Name" required>
						<br>
						<label for="Category">Category</label>
						<input type = "text" name = "Category" placeholder = "Category" required>
						<br>
						<label for="time_between_flows">Time between flows</label>
						<input type = "text" name = "time_between_flows" placeholder = "Time between flows">
						<br>
						<label for="no_required_flows">Number required flows</label>
						<input type = "number" name = "no_required_flows" placeholder = "Number Required flows">
						<br><br>
						<input type = "submit" name = "enter_app" value = "Add Application">
					</form>
				</div>

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

						if(empty($time_between) and empty($no_required)){
							$sql = "INSERT INTO application_type (Application_name, Category) VALUES ('$app_name', '$Category');";
						}
						elseif(empty($time_between)){
							$sql = "INSERT INTO application_type (Application_name, Category, no_required_flows) VALUES ('$app_name', '$Category', '$no_required');";
						}elseif(empty($no_required)){
							$sql = "INSERT INTO application_type (Application_name, Category, time_between_flows) VALUES ('$app_name', '$Category', '$time_between');";
						}else{
							$sql = "INSERT INTO application_type (Application_name, Category, time_between_flows, no_required_flows) VALUES ('$app_name', '$Category', '$time_between', '$no_required');";
						}
						
						if(!mysqli_query($conn, $sql)){
							echo "There was an error. Please try again";
						}else{
							echo "App added";
							echo "<meta http-equiv='refresh' content='0'>";
						}
						
					} 

				?>
			</div>
		</div>

		<div class = "row">
			<h2>Names table</h2>
			<table class="display">
					<tr>
						<th>IP Address</th>
						<th>AS Name</th>
						<th>NS Name</th>
						<th >Application Type</th>
					</tr>
					<?php
						$appSelect = mysqli_query($conn, "SELECT name_table.IP_address, name_table.AS_name, name_table.NS_name, application_type.Application_name FROM name_table INNER JOIN application_type on name_table.App_ID = application_type.App_ID;");
						if(mysqli_num_rows($appSelect) > 0){
							while($row = mysqli_fetch_array($appSelect)){
					?>
					<tr>
				        	<td><?php echo $row["IP_address"]; ?></td>
				        	<td><?php echo $row["AS_name"]; ?></td>
						<td><?php echo $row["NS_name"]; ?></td>
						<td><?php echo $row["Application_name"]; ?></td>
					</tr>
					<?php
							}
						}
						else{
							echo "No results found";
						}
					?>
				</table>

		</div>
	
		
	</body>
<html>


