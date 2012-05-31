var map;

function initialize() {
	console.log('Google Maps Init');
	var myOptions = getMapInitOptions();
	map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);
	google.maps.event.addListener(map, 'center_changed', function() {
		// 3 seconds after the center of the map has changed, pan back to the
		// marker.
		window.setTimeout(function() {
			updateFormDate(map)
		}, 1000);
	});
	google.maps.event.addListener(map, 'bounds_changed', function() {
		// 3 seconds after the center of the map has changed, pan back to the
		// marker.
		window.setTimeout(function() {
			updateFormDate(map)
		}, 1000);
	});
	google.maps.event.addListener(map, 'click', function(event) {
		placeMarker(event.latLng);
	});
	updateFormDate(map)
}

function getMapInitOptions() {
	var myOptions = {
		center : new google.maps.LatLng(8.9, -80.2),
		zoom : 8,
		mapTypeId : google.maps.MapTypeId.ROADMAP
	};
	lastExtent = JSON.parse(jQuery.cookie('last-extent'));
	if (lastExtent != null) {
		myOptions = {
			center : new google.maps.LatLng(lastExtent.latitude,
					lastExtent.longitude),
			zoom : lastExtent.zoom,
			mapTypeId : google.maps.MapTypeId.ROADMAP
		};
	}
	return myOptions;
}
// $('body').load(initialize);
function updateFormDate(map) {
	$('#loc-name').attr('value',"");
	$('#latitude').attr('value',map.getCenter().lat());
	$('#longitude').attr('value',map.getCenter().lng());
	$('#zoom').attr('value',map.getZoom());
	
	$("#lat-display").text(displayDMS(map.getCenter().lat(), 'lat'));
	$("#lng-display").text(displayDMS(map.getCenter().lng(), 'lng'));
	$("#zoom-display").text(map.getZoom());

	lastExtent = {
		'latitude' : map.getCenter().lat(),
		'longitude' : map.getCenter().lng(),
		'zoom' : map.getZoom()
	};
	$.cookie('last-extent', JSON.stringify(lastExtent), { path: '/' });


}
function displayDMS(deg, type){
	c =" ";
	if (deg < 0 && type == 'lat'){
		c ="S";
	}else if(deg > 0 && type == 'lat'){
		c = "N"
	}else if(deg > 0 && type == 'lng'){
		c = "E"
	}else if(deg < 0 && type == 'lng'){
		c = "W"
	}
	d = Math.floor(Math.abs(deg));
	mindec = (Math.abs(deg) -d) * 60.0;
	min = Math.floor(mindec);
	secdec = Math.round((mindec - min) * 60.0 * 10000)/10000;
	return c + " " +d +"° " + min + "\" " + secdec + "'";
	
}
function placeMarker(location) {
	var marker = new google.maps.Marker({
		position : location,
		map : map
	});
	$("#dialog-message").dialog('open');
}