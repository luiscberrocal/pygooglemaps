//utf-8

function deleteLocation(event) {
	// alert("Delete " + event.data.id + " is not implemented");
	dataString = "id=" + event.data.id
	$.ajax({
		type : "POST",
		url : "/delete-locations.json",
		dataType : "json",
		data : dataString,
		success : function(data) {
			var ename = "#location_" + event.data.id;
			$(ename).remove();
			// alert("Deleted " + data.date + " id: " + data.id);
		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error: " + errorThrown + "\nTextStatus: " + textStatus)
		}
	});
}
function zoomToLocation(event) {
	// alert(event.data.name);
	center = new google.maps.LatLng(event.data.latitude, event.data.longitude)
	map.setCenter(center);
	map.setZoom(event.data.zoom);
}
function loadLocations(data) {
	$('#saved-locations').empty()
	for ( var i = 0; i < data.length; i++) {
		locationDiv = $('<div/>', {
			'class' : 'location',
			'id' : 'location_' + data[i].id
		});
		locationNameDiv = $('<div/>', {
			'class' : 'location-name'
		});
		locationNameDiv.text(data[i].name);
		locationDiv.append(locationNameDiv)
		// Zoom Button
		zoomButton = $('<button/>', {
			'class' : 'zoom'
		});
		zoomButton.text('Zoom');
		zoomButton.bind('click', {
			id : data[i].id,
			name : data[i].name,
			latitude : data[i].latitude,
			longitude : data[i].longitude,
			zoom : data[i].zoom
		}, zoomToLocation);
		deleteButton = $('<button/>', {
			'class' : 'delete'
		});
		deleteButton.text('Delete');
		deleteButton.bind('click', {
			id : data[i].id,
			name : data[i].name
		}, deleteLocation);
		locationDiv.append(locationNameDiv);
		locationDiv.append(zoomButton);
		locationDiv.append(deleteButton);
		$('#saved-locations').append(locationDiv)
	}
}