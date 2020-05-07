header, body {
	background-color: #F0F0F0;
}

ul {
	list-style-type: none;
	margin:0;
	padding:0;
	overflow: hidden;
	background-color: purple;
}

li {
	float: left;
	border-right: 1px solid white;
}
 
li a{
	display: block;
	color: white;
	text-align:center;
	padding:14px 16px;
	text-decoration:none;
	
}

li a:hover {
	background-color: black;
}

table.display td, table.display th {
	border: 1px solid #ddd;
	padding: 8px;
}

tr:nth-child(even){
	background-color: #E0E0E0;
}

tr:hover{
	background-color: #C0C0C0;
}

th{
	padding-top: 12px;
	padding-bottom: 12px;
	text-align: left;
	background-color: purple;
	color: white;
}



.INSERT input[type=text], .INSERT input[type=number], select, textarea {
	width: 90%;
	padding: 12px 20px;
	border: 1px solid #ccc;
	border-radius: 4px;
}

label {
	
	display: inline-block;
	font-size: 16px;
	font-weight: bold;
	padding: 5px;
}

.INSERT input[type=submit] {
	background-color: purple;
	color:white;
	padding: 12px 20px;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	width:100%;
}

.INSERT input[type=submit]:hover {
	background-color: #45a049;
}

input[type=submit] {
	background-color: purple;
	color:white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}

input[type=submit]:hover {
	background-color: #45a049;
}

.INSERT {
	border-radius: 5px;
	background-color: #E0E0E0;
	padding:20px;
	width: 50%;
	resize: vertical;
}

.column{
	margin: 5px;
	float: left;
}

.column.left{
	width: 44%
}

.column.right {
	width: 54%;
}

.BothColumns:after{
	clear:both;
}

.row{
	padding-left: 450px;
	clear:both;
}
