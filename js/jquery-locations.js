//utf-8
// By L. Berrocal

function onJQueryDocumentReady() {
	console.debug('JQuery Document ready');
	$("#location-form").submit(function(e) {
		e.preventDefault();
		var dataString = $(this).serialize();
		$("#debug-output").text(dataString);
		$.ajax({
			type : "POST",
			url : "/add-location.html",
			dataType : "json",
			data : dataString,
			success : function(data) {
				// alert("Saved " + data.date + " id: " + data.id);
				// locationDiv = buildLocationDiv(data);
				getLocationsFromBackend();

			},
			error : function(jqXHR, textStatus, errorThrown) {
				alert("Error: " + errorThrown + "\nTextStatus: " + textStatus)
			}
		});
		
	});
	getLocationsFromBackend();
	
	$("#dialog-message").dialog({
		modal : true,
		buttons : {
			Ok : function() {
				$(this).dialog("close");
			}
		}
	});
}
function getLocationsFromBackend() {
	$.ajax({
		type : "GET",
		url : "/list-locations.json",
		dataType : "json",
		success : loadLocations
	});
}
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

function buildLocationDiv(data) {
	locationDiv = $('<div/>', {
		'class' : 'location',
		'id' : 'location_' + data.id
	});
	locationNameDiv = $('<div/>', {
		'class' : 'location-name'
	});
	locationNameDiv.text(data.name);
	locationDiv.append(locationNameDiv)
	// Zoom Button
	zoomButton = $('<button/>', {
		'class' : 'zoom'
	});
	zoomButton.text('Zoom');
	zoomButton.bind('click', {
		id : data.id,
		name : data.name,
		latitude : data.latitude,
		longitude : data.longitude,
		zoom : data.zoom
	}, zoomToLocation);
	deleteButton = $('<button/>', {
		'class' : 'delete'
	});
	deleteButton.text('Delete');
	deleteButton.bind('click', {
		id : data.id,
		name : data.name
	}, deleteLocation);
	locationDiv.append(locationNameDiv);
	locationDiv.append(zoomButton);
	locationDiv.append(deleteButton);
	return locationDiv;
}
function loadLocations(data) {
	$('#saved-locations').empty()
	for ( var i = 0; i < data.length; i++) {
		locationDiv = buildLocationDiv(data[i])
		$('#saved-locations').append(locationDiv)
	}
}