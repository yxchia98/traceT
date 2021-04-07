const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function getDate(){
  var today = new Date();
  var hour = today.getHours();
  var meridian;
  
  if (hour >= 12)
  {
	  meridian = 'PM';
	  hour -= 12;
  }
  else
  {
	  meridian = 'AM';
  }
  
  var date = today.getDate() + " " + monthNames[today.getMonth()] + " " + today.getUTCFullYear();
  var time = hour + ":" + today.getMinutes() + meridian;
  document.getElementById("currentDate").innerHTML = date;
  document.getElementById("currentTime").innerHTML = time;
}

getDate();