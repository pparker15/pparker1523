
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
		 <title>Flows</title>
	</head>

	<body>
		<table style="width:100%; border:1px solid black;">
			<tr>
				<th style="border:1px solid black;">Flow Timestamp</th>
				<th style="border:1px solid black;">Source Name</th>
				<th style="border:1px solid black;">Destination Name</th>
				<th style="border:1px solid black;">Category</th>
				<th style="border:1px solid black;">Associated</th>
			</tr>
			<?php
				$appSelect = mysqli_query($conn, "SELECT Flow_ID, Flow_Date_Time, Source_Name, Destination_Name, Flow_Category,(SELECT GROUP_CONCAT(Application_name) from application_type a, Associated b where a.App_ID = b.Associated_App_ID and b.Flow_ID = c.Flow_ID) as Associated from Flows c;");
				if(mysqli_num_rows($appSelect) > 0){
					while($row = mysqli_fetch_array($appSelect)){
			?>
			<tr>
                        	<td style="border:1px solid black;"><?php echo $row["Flow_Date_Time"]; ?></td>
                        	<td style="border:1px solid black;"><?php echo $row["Source_Name"]; ?></td>
				<td style="border:1px solid black;"><?php echo $row["Destination_Name"]; ?></td>
				<td style="border:1px solid black;"><?php echo $row["Flow_Category"]; ?></td>
				<td style="border:1px solid black;"><?php echo $row["Associated"]; ?></td>
			</tr>
			<?php
					}
				}
				else{
					echo "No results found";
				}
			?>
		</table>
	</body>
<html>
