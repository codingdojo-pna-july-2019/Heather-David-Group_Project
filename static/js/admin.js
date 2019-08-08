$(document).ready(function() {
	// ***********************
    // 	   LOAD ALL FORMS 
    // ***********************
    $.get( '/admin/food' ).done(function(data) {
    	$('#frmFoodContainer').html( data );
    });
    $.get( '/admin/beer' ).done(function(data) {
    	$('#frmBeerContainer').html( data );
    });
    $.get( '/admin/liquor' ).done(function(data) {
    	$('#frmLiquorContainer').html( data );
    });
    
    // ***********************
    // 	 FOOD FORM CONTROLS 
    // ***********************
    // New Food form
    $(document).on("click", "button[name='btn_new_food']", function() {
    	$.post( '/update/food', $('#frmNewFood').serialize())
        	.done(function(data) {
        		$('#frmFoodContainer').empty();
        		$('#frmFoodContainer').html( data );
        	});
    });

    // Update Food Status form
    $(document).on("click", "button[name='btn_status_food']", function() {
    	$.post( '/update/food', $('#frmUpdateFood').serialize())
        	.done(function(data) {
        		$('#frmFoodContainer').empty();
        		$('#frmFoodContainer').html( data );
        	});
    });

    // Delete Food form
    $(document).on("click", "button[name='btn_delete_food']", function() {
    	$('input[name="food_id"]').val( $(this).prop("id") );
    	$.post( '/update/food', $('#frmDeleteFood').serialize())
        	.done(function(data) {
        		$('#frmFoodContainer').empty();
        		$('#frmFoodContainer').html( data );
        	});
    });

    // ***********************
    // 	 BEER FORM CONTROLS 
    // ***********************
    // New Beer form
    $(document).on("click", "button[name='btn_new_beer']", function() {
    	$.post( '/update/beer', $('#frmNewBeer').serialize())
        	.done(function(data) {
        		$('#frmBeerContainer').empty();
        		$('#frmBeerContainer').html( data );
        	});
    });

    // Update Beer Status form
    $(document).on("click", "button[name='btn_status_beer']", function() {
    	$.post( '/update/beer', $('#frmUpdateBeer').serialize())
        	.done(function(data) {
        		$('#frmBeerContainer').empty();
        		$('#frmBeerContainer').html( data );
        	});
    });

    // Delete Beer form
    $(document).on("click", "button[name='btn_delete_beer']", function() {
    	$('input[name="beer_id"]').val( $(this).prop("id") );
    	$.post( '/update/beer', $('#frmDeleteBeer').serialize())
        	.done(function(data) {
        		$('#frmBeerContainer').empty();
        		$('#frmBeerContainer').html( data );
        	});
    });

    // ************************
    // 	 LIQUOR FORM CONTROLS 
    // ************************
    // New Liquor form
    $(document).on("click", "button[name='btn_new_liq']", function() {
    	$.post( '/update/liquor', $('#frmNewLiquor').serialize())
        	.done(function(data) {
        		$('#frmLiquorContainer').empty();
        		$('#frmLiquorContainer').html( data );
        	});
    });

    // Update Liquor Status form
    $(document).on("click", "button[name='btn_status_liq']", function() {
    	$.post( '/update/liquor', $('#frmUpdateLiquor').serialize())
        	.done(function(data) {
        		$('#frmLiquorContainer').empty();
        		$('#frmLiquorContainer').html( data );
        	});
    });

    // Delete Liquor form
    $(document).on("click", "button[name='btn_delete_liq']", function() {
    	$('input[name="liq_id"]').val( $(this).prop("id") );
    	$.post( '/update/liquor', $('#frmDeleteLiquor').serialize())
        	.done(function(data) {
        		$('#frmLiquorContainer').empty();
        		$('#frmLiquorContainer').html( data );
        	});
    });

});