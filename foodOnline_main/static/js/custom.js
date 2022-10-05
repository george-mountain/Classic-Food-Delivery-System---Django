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
                            response.cart_amount['tax'],
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
                    response.cart_amount['tax'],
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
                    response.cart_amount['tax'],
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
    function applyCartAmounts(subtotal,tax,grand_total){
        // Run this function if the user is on the cart page
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }

        
    }
});