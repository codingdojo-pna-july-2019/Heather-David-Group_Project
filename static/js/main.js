$(document).ready( function() {

	$('[name="tweet"]').each( function() {
		var tweet = $(this)[0];
		var id = tweet.getAttribute("tweetID");

		twttr.widgets.createTweet(
			id, tweet, 
			{
				conversation : 'none',    // or all
				cards        : 'hidden',  // or visible 
				linkColor    : '#cc0000', // default is blue
				theme        : 'dark'    // or light
			})
		.then (function (el) {
			// el.contentDocument.querySelector(".footer").style.display = "none";
		});
	});

});