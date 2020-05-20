<?php
	# Database connection.
	$DB_SERVER = 'localhost:3306';
	$DB_USERNAME = 'parker';
	$DB_PASSWORD = 'password';
	$DB_DATABASE = 'application_identification';
	
	$conn = mysqli_connect($DB_SERVER, $DB_USERNAME, $DB_PASSWORD, $DB_DATABASE);
?>

<!DOCTYPE HTML>
<html>
	<head>
		<title>Home Page</title>
		<link rel="stylesheet" type="text/css" href="stylesheet.css">

		<!--Google Charts-->
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    		
		<!--Graph 1 - Flows per category-->
 		<script type="text/javascript">
 			google.load("visualization", {packages:["corechart"]});
 			google.setOnLoadCallback(drawChart);
			 function drawChart() {
				 var data = google.visualization.arrayToDataTable([
				 ['Category','Flows'],
				 <?php 
					 $query = "SELECT Flow_Category, COUNT(*) AS 'count' FROM Flows GROUP BY Flow_Category";
					 $exec = mysqli_query($conn,$query);
					 while($row = mysqli_fetch_array($exec)){
					 	echo "['".$row['Flow_Category']."',".$row['count']."],";
					 }
				 ?> 
			 	]);
			 	var options = {
			 		title: 'Percentage of flows per category',
					is3D: true

			 	};
			 	var chart = new google.visualization.PieChart(document.getElementById("piechart"));
				chart.draw(data,options);
			 }
    		</script>
		
		<!--Graph 2 - Flows per application-->
		<script type="text/javascript">
 			google.load("visualization", {packages:["corechart"]});
 			google.setOnLoadCallback(drawChart);
			 function drawChart() {
				 var data = google.visualization.arrayToDataTable([
				 ['Application_Name','Count'],
				 <?php 
					 $query = "SELECT Application_name, App_Count FROM application_type WHERE Category != 'USERS';";
					 $exec = mysqli_query($conn,$query);
					 while($row = mysqli_fetch_array($exec)){
					 	echo "['".$row['Application_name']."',".$row['App_Count']."],";
					 }
				 ?> 
			 	]);
			 	var options = {
			 		title: 'Percentage of flows using application as either source or destination',
					is3D: true

			 	};
			 	var chart = new google.visualization.PieChart(document.getElementById("piechart3"));
				chart.draw(data,options);
			 }
    		</script>

		<!--Graph 3 - Associated Flows-->
		<script type="text/javascript">
 			google.load("visualization", {packages:["corechart"]});
 			google.setOnLoadCallback(drawChart);
			 function drawChart() {
				 var data = google.visualization.arrayToDataTable([
				 ['Category','Flows'],
				 <?php 
					# Get the application names.
					$getID = mysqli_query($conn, "SELECT App_ID, Application_name FROM application_type WHERE NOT Category = 'NETWORK' AND NOT Category = 'USERS' AND NOT Category = 'CDN' AND NOT Category = 'UNKNOWN';");
					# Count the associated flows with the application names from previous query.
					while($idRow = mysqli_fetch_array($getID)){
						$aid = $idRow['App_ID'];
						$query = "SELECT Count(*) as count FROM Associated WHERE Associated_App_ID = '$aid';";
						$exec = mysqli_query($conn,$query);
						while($row = mysqli_fetch_array($exec)){
							$count = $row['count'];
							echo "['".$idRow['Application_name']."',$count],";
						}
						
					}
					# Calculate the number of unassociated flows.
					$numbers = "SELECT(SELECT DISTINCT Count(Flow_ID) FROM Associated) as count_flow_ID, (SELECT Count(*) From Flows WHERE Flow_Category = 'Unknown' or Flow_Category = 'CDN') as total_count;";	
					$execNumbers = mysqli_query($conn, $numbers);
					while($numberResult = mysqli_fetch_array($execNumbers)){
						$calcNumber = $numberResult['total_count'] - $numberResult['count_flow_ID'];
						echo "['Unassociated',$calcNumber],";
					}			 
					 
				 ?> 
			 	]);
			 	var options = {
			 		title: 'Percentage traffic associated with each application',
					is3D: true

			 	};
			 	var chart = new google.visualization.PieChart(document.getElementById("piechart2"));
				chart.draw(data,options);
			 }
    		</script>

		
	</head>
	<!--Navigation Bar-->
	<header>
		<ul>
			<li><a href='index.php'>Home Page</a></li>
      			<li><a href='flows_page.php'>Flows</a></li>
      			<li><a href='Application_Input.php'>Applications</a></li>
		</ul>
	</header>
	<body>
		<h1>Quick summary</h1>
		<h3>Percentage application is likely to be the different categories </h3>
		<?php
			# Display percentage of associated flows per category for each CDN
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
		<br><br>
		<!--Display the graphs on the page-->
		  <div class="container-fluid">
			 <div id="piechart" style="width: 100%; height: 500px;"></div>
			 <div id="piechart3" style="width: 100%; height: 500px;"></div>
			 <div id="piechart2" style="width: 100%; height: 500px;"></div>
		 </div>

		
		
	</body>
</html>
