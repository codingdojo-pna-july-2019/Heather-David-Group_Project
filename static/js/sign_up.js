$(document).ready(function() {
	var timerFN, timerLN, timerUN, timerEM, timerPW, timerPWC;

    $('input[name="fname"]').keyup(function() {
    	clearTimeout(timerFN);
    	timerFN = setTimeout(function() {
    		$.post( '/ajax/validate/user_first_name', $('#frmSignUp').serialize())
	        	.done(function(data) {
	        		$('#err_msg_fname').empty();
	        		$('#err_msg_fname').html( data );
	        		validateForm();
	        	});
    	}, 1000);
    });
	$('input[name="lname"]').keyup(function() {
		clearTimeout(timerLN);
    	timerLN = setTimeout(function() {
			$.post( '/ajax/validate/user_last_name', $('#frmSignUp').serialize())
	        	.done(function(data) {
	        		$('#err_msg_lname').empty();
	        		$('#err_msg_lname').html( data );
	        		validateForm();
	        	});
		}, 1000);
	});
	$('input[name="uname"]').keyup(function() {
		clearTimeout(timerUN);
    	timerUN = setTimeout(function() {
			$.post( '/ajax/validate/user_name', $('#frmSignUp').serialize())
	        	.done(function(data) {
	        		$('#err_msg_uname').empty();
	        		$('#err_msg_uname').html( data );
	        		validateForm();
	        	});
		}, 1000);
	});
	$('input[name="email"]').keyup(function() {
		clearTimeout(timerEM);
    	timerEM = setTimeout(function() {
			$.post( '/ajax/validate/user_email', $('#frmSignUp').serialize())
	        	.done(function(data) {
	        		$('#err_msg_email').empty();
	        		$('#err_msg_email').html( data );
	        		validateForm();
	        	});
		}, 1000);
	});
	$('input[name="password"]').keyup(function() {
		clearTimeout(timerPW);
    	timerPW = setTimeout(function() {
			$.post( '/ajax/validate/user_password', $('#frmSignUp').serialize())
	        	.done(function(data) {
	        		$('#err_msg_pw').empty();
	        		$('#err_msg_pw').html( data );
	        		validateForm();
	        	});
		}, 1000);
	});
	$('input[name="confirm_password"]').keyup(function() {
		clearTimeout(timerPWC);
    	timerPWC = setTimeout(function() {
			$.post( '/ajax/validate/user_password_sameness', $('#frmSignUp').serialize())
	        	.done(function(data) {
	        		$('#err_msg_pw_confirm').empty();
	        		$('#err_msg_pw_confirm').html( data );
	        		validateForm();
	        	});
		}, 1000);
	});

});

function validateForm() {
	// No errors and all input fields entered
	if( $('[name="err_msg"]').length == 0 && $('input[name=fname]').val() != "" && $('input[name=lname]').val() != "" && $('input[name=uname]').val() != "" && $('input[name=email]').val() != "" && $('input[name=password]').val() != "" && $('input[name=confirm_password]').val() != "") {
		$(':submit').prop("disabled", false);
	} else {
		$(':submit').prop("disabled", true);
	}
}