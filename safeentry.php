<!DOCTYPE html>
<html lang="en">
<head>
  <title>SafeEntry</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <link rel="stylesheet" href="safeE.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</head>

<body>
<div class="jumbotron text-center">
  <h5>This is for demonstration purpose only.</h5>
  <h3>SafeEntry</h3>
  <img class=tt src="https://theme.zdassets.com/theme_assets/9722682/31cf771430adf7e5fc91e10d20819cb263c68e1d.png">
  <p class="tt">TraceTogether</p>
</div>
  
<div class="container" style="font-size: 150%">
  <div class="card">
    <div class="card-body" style="background-color:rgb(57, 196, 134); color: white; font-size:150%">SafeEntry Check-in</div>
  </div>
  <div class="card" style="border-background-left-radius: 25px">
    <div class="card-body">
	<img class="card-background" src="https://theme.zdassets.com/theme_assets/9722682/31cf771430adf7e5fc91e10d20819cb263c68e1d.png">
	  <p class="current date" id="currentDate"></p>
	  <p class="current time" id="currentTime"></p>
		<?php
			echo '<p class="current location">'.$_GET["location"].'</p>';
		?>
	  <script src="date.js"></script>
	</div>
  </div>
  <div class="checkinout">
  <button type="button" class="b2">CHECK OUT</button
  </div>	
</div>
</body>
</html>