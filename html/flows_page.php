<?php
	# Database connection.
	$DB_SERVER = 'localhost:3306';
	$DB_USERNAME = 'parker';
	$DB_PASSWORD = 'password';
	$DB_DATABASE = 'application_identification';
	
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
		<p>Search for flows using the categories provided. Select a field to use as part of the search criteria.</p>

		<p>*NOTE* Please wait for the page to load before scrolling through, which may take a while as there is a large amount of data. If there are no results, there may be to many rows.</p>

		<!--Form to filter the flows and associated applications-->	
		<form method = "POST" action='flows_page.php'>
			<label for="filter">Filter: </label>
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
		# Select flows from the database depending on data from the form.
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
			}
		}
		else {
			$sql= "SELECT Flow_ID, Flow_Date_Time, Source_Name, Destination_Name, Flow_Category,(SELECT GROUP_CONCAT(Application_name) from application_type a, Associated b where a.App_ID = b.Associated_App_ID and b.Flow_ID = c.Flow_ID) as Associated from Flows c;";
		}

	?>

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
		
</body>
</html>
