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

$(document).ready(function(){
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        
        url = $(this).attr('data-url'); 

        data = {
            food_id: food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response)
                if (response.status == 'login_required') {
                    // use sweetalert here
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                    
                }
                
                if(response.status == 'Failed'){
                    swal(response.message,'','error')

                }
                
                else {
                        // load the total cart count in real time to cart icon navbar
                        $('#cart_counter').html(response.cart_counter['cart_count']);
                        // load the quantity for each food item
                        $('#qty-'+food_id).html(response.qty);

                        // subtotal, tax and grand total: call the helper function
                        applyCartAmounts(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax_dict'],
                            response.cart_amount['grand_total']
                        )

                }
            }
        })
    })
    // Place the cart item quantity on load.
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })

    // decrease cart functionalities

    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        
        url = $(this).attr('data-url'); 
        // get cart id
        cart_id = $(this).attr('id');

        data = {
            food_id: food_id,
            cart_id : cart_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response)
                if (response.status == 'login_required') {
                    // use sweetalert here
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                    
                }
                else if (response.status == 'Failed') {
                    swal(response.message,'','error')
                } 
                
                else {
                    // load the total cart count in real time to cart icon navbar
                $('#cart_counter').html(response.cart_counter['cart_count']);
                // load the quantity for each food item
                $('#qty-'+food_id).html(response.qty);

                // subtotal, tax and grand total: call the helper function
                applyCartAmounts(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax_dict'],
                    response.cart_amount['grand_total']
                )

                // call helper function
                // Run these helper function for decrease cart if usr in cart page
                if(window.location.pathname == '/cart/'){
                removeCartItem(response.qty,cart_id);
                checkEmptyCart();
                }
            }
                
            }
        })
    })
    
    // delete cart item function
    $('.delete_cart').on('click',function(e){
        e.preventDefault();
        
        cart_id = $(this).attr('data-id');
        
        url = $(this).attr('data-url'); 

        data = {
            cart_id: cart_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response)
                if (response.status == 'Failed') {
                    swal(response.message,'','error')
                } 
                
                else {
                    // load the total cart count in real time to cart icon navbar
                $('#cart_counter').html(response.cart_counter['cart_count']);
                swal(response.status,response.message,"success")
                
                // subtotal, tax and grand total: call the helper function
                applyCartAmounts(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax_dict'],
                    response.cart_amount['grand_total']
                )
                // call the helper function
                removeCartItem(0,cart_id);
                checkEmptyCart();
                
                }
                
            }
        })
    })

    // helper function: delete the cart element if the quantity is 0
    function removeCartItem(cartItemQty,cart_id){
        
        if(cartItemQty <= 0){
            // remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }

    // check if the cart is empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0){
            document.getElementById('empty-cart').style.display = "block";
        }
    }

    // function to apply cart amounts dynamically on the cart html page
    function applyCartAmounts(subtotal,tax_dict,grand_total){
        // Run this function if the user is on the cart page
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#total').html(grand_total)

            for(key1 in tax_dict){
                console.log(tax_dict[key1])
                for(key2 in tax_dict[key1]){
                    $('#tax-'+key1).html(tax_dict[key1][key2])
                }
            }
        }

        
    }

    // Add opening hour functionality
    $('.add_hour').on('click',function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var url = document.getElementById('add_hour_url').value 
        // handle/capture the CSRF token associated with this form
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        console.log(day,from_hour,to_hour,is_closed,csrf_token)

        // Validate form field - Check empty field etc
        if (is_closed) {
            is_closed = 'True'
            condition = "day != ''"
            
        } else {
            is_closed = 'False'
            condition = "day !='' && from_hour != '' && to_hour != ''"
            
        }

        if (eval(condition)) {
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken':csrf_token
                },
                success: function(response){
                    if(response.status == 'success'){
                        // Append the data received from the view response to the table of opening hour html page dynamically
                        if (response.is_closed == 'Closed') {
                            html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td> <td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';
                        } else {
                            html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td> <td><a href="#" class="remove_hour" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';
                        }
                        
                        $(".opening_hours").append(html)

                        // Reset the form now
                        document.getElementById("opening_hours").reset()

                    }else{
                        swal(response.message,'',"error")
                    }
                }
            })
        } else {
            swal('Please fill all the fields', '', 'info')
        }
    });

    // Remove Opeining Hours

    $(document).on('click','.remove_hour',function(e){
        e.preventDefault();
        url = $(this).attr('data-url');
        
        // Send to the view function via ajax
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                // if deletion from database is successful, remove tr element
                if(response.status == 'success'){
                    document.getElementById('hour-'+response.id).remove()
                }
            }
        })
    })


    // ending of document ready function
});