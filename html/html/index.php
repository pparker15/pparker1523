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
		 <title>Graphs</title>
		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    		
 		<script type="text/javascript">
 			google.load("visualization", {packages:["corechart"]});
 			google.setOnLoadCallback(drawChart);
			 function drawChart() {
				 var data = google.visualization.arrayToDataTable([
				 ['Category','Flows'],
				 <?php 
					 $query = "SELECT Category, COUNT(*) AS 'count' FROM processed_nfdump_data GROUP BY Category";
					 $exec = mysqli_query($conn,$query);
					 while($row = mysqli_fetch_array($exec)){
					 	echo "['".$row['Category']."',".$row['count']."],";
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
		<script type="text/javascript">
 			google.load("visualization", {packages:["corechart"]});
 			google.setOnLoadCallback(drawChart);
			 function drawChart() {
				 var data = google.visualization.arrayToDataTable([
				 ['Category','Flows'],
				 <?php 
					 $query = "SELECT (SELECT COUNT(*) FROM processed_nfdump_data WHERE Associated_1 = 'SPOTIFY' or Associated_2 = 'SPOTIFY' or Associated_3 = 'SPOTIFY' ) as 'count_spotify', (SELECT COUNT(*) FROM processed_nfdump_data WHERE Associated_1 ='FACEBOOK' or Associated_2 = 'FACEBOOK' or Associated_3 = 'FACEBOOK' ) as 'count_facebook', (SELECT COUNT(*) FROM processed_nfdump_data WHERE Associated_1 ='TWITTER' or Associated_2 = 'TWITTER' or Associated_3 = 'TWITTER' ) as 'count_twitter', (SELECT COUNT(*) FROM processed_nfdump_data WHERE Associated_1 ='BBC' or Associated_2 = 'BBC' or Associated_3 = 'BBC' ) as 'count_BBC', (SELECT COUNT(*) FROM processed_nfdump_data WHERE Associated_1 =' ') as 'count_blank'";

					 $exec = mysqli_query($conn,$query);
					 while($row = mysqli_fetch_array($exec)){
					 	echo "['Spotify',".$row['count_spotify']."],";
						echo "['Facebook',".$row['count_facebook']."],";
						echo "['Twitter',".$row['count_twitter']."],";
						echo "['BBC',".$row['count_BBC']."],";
						echo "['No association',".$row['count_blank']."],";
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

		<script type="text/javascript">
 			google.load("visualization", {packages:["corechart", "line"]});
 			google.setOnLoadCallback(drawChart);
			 function drawChart() {
				 var data = google.visualization.arrayToDataTable([
				 ['Time','No. Flows'],
				 <?php 
					 $query = "SELECT COUNT(*) as 'count', date_time_flow_less_specific FROM processed_nfdump_data GROUP BY date_time_flow_less_specific";
					 $exec = mysqli_query($conn,$query);
					 while($row = mysqli_fetch_array($exec)){
					 	echo "['".$row['date_time_flow_less_specific']."',".$row['count']."],";
					 }
				 ?> 
			 	]);
			 	var options = {
			 		title: 'Number of flows over time',
					curveType: 'function',
          				legend: { position: 'bottom' }

			 	};
			 	var chart = new google.visualization.LineChart(document.getElementById("linechart"));
				chart.draw(data,options);
			 }
    		</script>
	</head>
	<body>
		 <div class="container-fluid">
		 <div id="piechart" style="width: 100%; height: 500px;"></div>
		 <div id="piechart2" style="width: 100%; height: 500px;"></div>
		 <div id="linechart" style="width: 800px; height: 700px;"></div>
		 </div>
	</body>
</html>



