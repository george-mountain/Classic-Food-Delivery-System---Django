let autocomplete;

function	initAutoComplete(){
	autocomplete = new google.maps.places.Autocomplete(
		document.getElementById('id_address'),
		{
			types: ['geocode','establishment'],
			// specify your country code here
			componentRestrictions: {'country':['in','jp','ng']},
		}
		)
	// function to specify what should happen when the prediction is clicked
	autocomplete.addListener('place_changed',onPlaceChanged);
}

function onPlaceChanged(){
	var place = autocomplete.getPlace();

	// User did not select the prediction. Reset the input field or alert()

	if(!place.geometry){
		document.getElementById('id_address').placeholder = "Start typing..."
	}
	else{
		console.log('place name=>',place.name)
	}
    
    // get the address components and assign them to the fields.
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value 

    geocoder.geocode({'address':address},function(results,status){
        // console.log('result=>',results)
        // console.log('status=>',status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>',latitude);
            // console.log('long=>',longitude);
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);
        }
    });
    //loop through the address components and assign other address data
    for(var i=0; i<place.address_components.length;i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            // Get the country name
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }

            // Get the state name
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }

            // Get the city name
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }

            // Get the country name
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }
}