<!DOCTYPE html>
<html lang="en">
<head>
  <title>SafeEntry</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</head>

<body>
<div style="text-align: center">
	<h2>SafeEntry Check In</h2>
	<form action="/safeentry.php">
	  <label for="name">ID:</label><br>
	  <input type="text" id="id" name="id" placeholder="Enter ID"><br>
	  <label for="name">Name:</label><br>
	  <input type="text" id="name" name="name" placeholder="Enter Full Name"><br>
	  <?php 
		$clicked = '';
		$loc = $_GET['location'];
		if(isset($loc)) 
          $clicked = $loc; 
	  ?>
	  <input type="hidden" name="location" value="<?php echo (isset($clicked)) ?  $clicked : '' ?>" /><br>
	  <input type="submit" value="Submit">
	</form> 
</div>
</body>
</html>
