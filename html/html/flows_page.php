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
		<title>Flows search</title>
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
	<div class = "column">
	<h1>Flows</h1>
		<form method = "POST" action='flows_page.php'>
			<label for="source">Source name</label>
			<input type="radio" id="src_Name" name = "filter" value ="srcName">
			<label for="Destination">Destination Name</label>
			<input type="radio" id="Destination" name = "filter" value ="dstName">
			<label for="DestinationSource">Source and Destination</label>
			<input type="radio" id="DestinationSource" name = "filter" value ="dstSRC">		
			<label for="Category">Category</label>
			<input type="radio" id="Category" name = "filter" value ="cat">
			<br>
			<input type="text" placeholder="Search..." name = "search">
			<input type='submit' value='Go' name='btnSearch'>
		</form>

	<?php
		$filter = $_POST['filter'];
		$search = $_POST['search'];
		if(isset($_POST['btnSearch'])){
			switch ($filter){
				case "srcName":
					$sql= "SELECT Flow_ID, Flow_Date_Time, Source_Name, Destination_Name, Flow_Category,(SELECT GROUP_CONCAT(Application_name) from application_type a, Associated b where a.App_ID = b.Associated_App_ID and b.Flow_ID = c.Flow_ID) as Associated from Flows c where c.Source_Name = '$search';";
					break;
				case "dstName":
					$sql= "SELECT Flow_ID, Flow_Date_Time, Source_Name, Destination_Name, Flow_Category,(SELECT GROUP_CONCAT(Application_name) from application_type a, Associated b where a.App_ID = b.Associated_App_ID and b.Flow_ID = c.Flow_ID) as Associated from Flows c where c.Destination_Name = '$search';";
					break;
				case "cat":
					$sql= "SELECT Flow_ID, Flow_Date_Time, Source_Name, Destination_Name, Flow_Category,(SELECT GROUP_CONCAT(Application_name) from application_type a, Associated b where a.App_ID = b.Associated_App_ID and b.Flow_ID = c.Flow_ID) as Associated from Flows c where c.Flow_Category = '$search';";
					break;
				case "associated":
					echo"Associated coming soon";
					break;
				case "dstSRC":
					$sql= "SELECT Flow_ID, Flow_Date_Time, Source_Name, Destination_Name, Flow_Category,(SELECT GROUP_CONCAT(Application_name) from application_type a, Associated b where a.App_ID = b.Associated_App_ID and b.Flow_ID = c.Flow_ID) as Associated from Flows c where c.Source_Name = '$search' or c.Destination_Name = '$search'";
					break;
				default:
					$sql= "SELECT Flow_ID, Flow_Date_Time, Source_Name, Destination_Name, Flow_Category,(SELECT GROUP_CONCAT(Application_name) from application_type a, Associated b where a.App_ID = b.Associated_App_ID and b.Flow_ID = c.Flow_ID) as Associated from Flows c;";
					break;

			}
		}

	?>

	<table>
			<tr>
				<th>Flow Timestamp</th>
				<th>Source Name</th>
				<th>Destination Name</th>
				<th>Category</th>
				<th>Associated</th>
			</tr>
			<?php
				$appSelect = mysqli_query($conn, $sql);
				if(mysqli_num_rows($appSelect) > 0){
					while($row = mysqli_fetch_array($appSelect)){
			?>
			<tr>
                        	<td><?php echo $row["Flow_Date_Time"]; ?></td>
                        	<td><?php echo $row["Source_Name"]; ?></td>
				<td><?php echo $row["Destination_Name"]; ?></td>
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
		<div class="column">
		<h1>Percentage application is likely to be the different categories </h1>
		<br><br><br>
		<?php
			$sql = "SELECT application_type.Application_name, stats_table.Assoc_News, stats_table.Assoc_Social_Media, stats_table.Assoc_Streaming FROM stats_table INNER JOIN application_type on stats_table.App_ID = application_type.App_ID;";

			$percent = mysqli_query($conn, $sql);
				if(mysqli_num_rows($percent) > 0){
					echo " <table>
						<tr>
						<th>Application Name</th>
						<th>News</th>
						<th>Social Media</th>
						<th>Streaming</th>
						</tr>";
					while($row = mysqli_fetch_array($percent)){
						$total = $row['Assoc_News'] + $row['Assoc_Social_Media']+$row['Assoc_Streaming'];
						$name = $row['Application_name'];
						$percentNews = ($row['Assoc_News'] / $total) * 100 ;
						$percentSocial = ($row['Assoc_Social_Media'] / $total) * 100 ;
						$percentStreaming = ($row['Assoc_Streaming'] / $total) * 100 ;
						echo "<tr>
						      <td>$name</td>
						      <td>$percentNews%</td>
						      <td>$percentSocial%</td>
						      <td>$percentStreaming%</td>
						      </tr>";	
					}
					echo "</table>";
				}

			
		?>
		</div>
</body>
</html>

