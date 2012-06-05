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

	$("#dialog-message").dialog(
			{
				modal : true,
				autoOpen : false,
				buttons : {
					"Save Point" : function() {
						var dataString = $("#point-form").serialize();
						// $("#debug-output").text(dataString);
						$.ajax({
							type : "POST",
							url : "/add-point.html",
							dataType : "json",
							data : dataString,
							success : function(data) {
								// getLocationsFromBackend();
								addMarkerToMap(data);
								locdiv = buildLocationDiv(data);
								$('#saved-locations').prepend(locdiv);

							},
							error : function(jqXHR, textStatus, errorThrown) {
								alert("Error: " + errorThrown
										+ "\nTextStatus: " + textStatus);
							}
						});
						$(this).dialog("close");
					},
					Cancel : function() {
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
			var ename = "#location_" + data.id;
			$(ename).remove();
			deleteMapOnLatLong(data.latitude, data.longitude)
		},
		error : function(jqXHR, textStatus, errorThrown) {
			alert("Error: " + errorThrown + "\nTextStatus: " + textStatus)
		}
	});
}

function deleteMapOnLatLong(latitude, longitude) {
	existingMarkerData = getMarkerInLatLong(latitude, longitude);
	if (existingMarkerData[0] != null) {
		existingMarkerData[0].setMap(null);
		delete markersArray[existingMarkerData[1]];
		markersArray.splice(existingMarkerData[1], 1);
	}
	// for ( var i = 0; i < markersArray.length; i++) {
	// if (markersArray[i].getPosition().lat() == latitude
	// && markersArray[i].getPosition().lng() == longitude) {
	// markersArray[i].setMap(null);
	// }
	// }
}
function zoomToLocation(event) {
	console.debug("Zoom to Location Type: " + event.data.loc_type);
	center = new google.maps.LatLng(event.data.latitude, event.data.longitude)
	map.setCenter(center);
	map.setZoom(event.data.zoom);
	if (event.data.loc_type == "point") {
		for ( var i = 0; i < markersArray.length; i++) {
			if (markersArray[i].getPosition().lat() == event.data.latitude
					&& markersArray[i].getPosition().lng() == event.data.longitude) {
				markersArray[i].setMap(map);
			}
		}
	}
}

function buildLocationDiv(data) {
	var divId = 'location_' + data.id;
	var locationDiv = $('<div/>', {
		'class' : 'location',
		'id' : divId
	});

	var locationNameDiv = $('<div/>', {
		'class' : 'location-name'
	});
	var loc_type_class = "loc-type-" + data.loc_type;
	locationNameDiv.addClass(loc_type_class);
	locationNameDiv.text(data.name);
	locationDiv.append(locationNameDiv)
	// Zoom Button
	var zoomButton = $('<button/>', {
		'class' : 'zoom'
	});
	zoomButton.text('Zoom');
	zoomButton.bind('click', {
		id : data.id,
		name : data.name,
		latitude : data.latitude,
		longitude : data.longitude,
		zoom : data.zoom,
		loc_type : data.loc_type
	}, zoomToLocation);
	var deleteButton = $('<button/>', {
		'class' : 'delete'
	});
	deleteButton.text('Delete');
	deleteButton.bind('click', {
		id : data.id,
		name : data.name,
		latitude : data.latitude,
		longitude : data.longitude
	}, deleteLocation);
	locationDiv.append(locationNameDiv);
	locationDiv.append(zoomButton);
	locationDiv.append(deleteButton);

	deleteButton.button({
		icons : {
			primary : "ui-icon-trash"
		},
		text : false
	});
	zoomButton.button({
		icons : {
			primary : "ui-icon-zoomin"
		},
		text : false
	});

	return locationDiv;
}
function loadLocations(data) {
	$('#saved-locations').empty()
	markersArray = [];
	for ( var i = 0; i < data.length; i++) {
		locationDiv = buildLocationDiv(data[i])
		$('#saved-locations').append(locationDiv);
		if (data[i].loc_type == "point") {
			addMarkerToMap(data[i]);
			// var marker = new google.maps.Marker({
			// position : new google.maps.LatLng(data[i].latitude,
			// data[i].longitude)
			// });
			//
			// markersArray.push(marker);
		}
	}
}
function getMarkerInLatLong(latitude, longitude) {
	var marker = null;
	var position = -1;
	for ( var i = 0; i < markersArray.length; i++) {
		if (markersArray[i].getPosition().lat() == latitude
				&& markersArray[i].getPosition().lng() == longitude) {
			marker = markersArray[i];
			break;
		}
	}
	return [ marker, position ];
}
function addMarkerToMap(data) {
	existingMarker = getMarkerInLatLong(data.latitude, data.longitude)[0];
	if (existingMarker == null) {
		latlng = new google.maps.LatLng(data.latitude, data.longitude);
		var marker = new google.maps.Marker({
			position : latlng,
			map : map,
			title : data.name
		});
		markersArray.push(marker);
	} else {
		existingMarker.setMap(map);
	}

}