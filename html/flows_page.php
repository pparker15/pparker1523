<?php
	# Database connection.
	$DB_SERVER = 'localhost:3306';
	$DB_USERNAME = 'parker';
	$DB_PASSWORD = 'password';
	$DB_DATABASE = 'user_profiling';
	
	$conn = mysqli_connect($DB_SERVER, $DB_USERNAME, $DB_PASSWORD, $DB_DATABASE);
?>

<!DOCTYPE html>
<html>
<head>
		<title>Flows search</title>
		<link rel="stylesheet" type="text/css" href="stylesheet.css">
	</head>

	<header>
		<!--Navigation Bar-->
		<ul>
			<li><a href='index.php'>Home Page</a></li>
      			<li><a href='flows_page.php'>Flows</a></li>
      			<li><a href='Application_Input.php'>Applications</a></li>
		</ul>
	</header>
<body>
	<div class = "column">
	<h1>Flows</h1>
		<p>View the flows and its associated applications</p>

		<p>*NOTE* Please wait for the page to load before scrolling through, which may take a while as there is a large amount of data.</p>

	<!--Display the data in a table-->
	<table>
			<tr>		
				<th>Flow Timestamp</th>
				<th>Source Name</th>
				<th>Destination Name</th>
				<th>Category</th>
				<th>Associated</th>
			</tr>
			<?php
				$sql= "SELECT Flow_ID, Flow_Date_Time, Source_Name_ID, Destination_Name_ID, Flow_Category,(SELECT GROUP_CONCAT(Application_name) from application_type a, Associated b where a.App_ID = b.Associated_App_ID and b.Flow_ID = c.Flow_ID) as Associated from Flows c;";
				$appSelect = mysqli_query($conn, $sql);
				if(mysqli_num_rows($appSelect) > 0){
					while($row = mysqli_fetch_array($appSelect)){
						# Get the source name	
						$FlowID = $row["Flow_ID"];
						$SourceQuery = "SELECT application_type.application_name FROM Flows INNER JOIN name_table on name_table.name_id = Flows.Source_Name_ID INNER JOIN application_type on application_type.App_ID = name_table.App_ID WHERE Flows.Flow_ID = '$FlowID'";
						$SourceNameSelect = mysqli_query($conn, $SourceQuery);
						$newRow = mysqli_fetch_array($SourceNameSelect);

						# Get the destination name
						$DestinationQuery = "SELECT application_type.application_name FROM Flows INNER JOIN name_table on name_table.name_id = Flows.Destination_Name_ID INNER JOIN application_type on application_type.App_ID = name_table.App_ID WHERE Flows.Flow_ID = '$FlowID'";
						$DestinationNameSelect = mysqli_query($conn, $DestinationQuery);
						$newRow2 = mysqli_fetch_array($DestinationNameSelect);

			?>
			<tr>                    	
				<td><?php echo $row["Flow_Date_Time"]; ?></td>
				<td><?php echo $newRow["application_name"]; ?></td>
				<td><?php echo $newRow2["application_name"]; ?></td>
				<td><?php echo $row["Flow_Category"]; ?></td>
				<td><?php echo $row["Associated"]; ?></td>
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
</html>


