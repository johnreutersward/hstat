$( document ).ready(function() {

	function getLive() {
		$.ajax({ 
			url: "/live", 
			cache: false 
		}).done( function( html ) {
	  		$("#live").html(html);
		});	
	}

	getLive();

	setInterval(function() {
    	getLive();	
	}, 30000);
	
});