$(document).ready( function() {

	// var tweet = document.getElementById("tweet");
	// var id = tweet.getAttribute("tweetID");

	// twttr.widgets.createTweet(
	// 	id, tweet, 
	// 	{
	// 		conversation : 'none',    // or all
	// 		cards        : 'hidden',  // or visible 
	// 		linkColor    : '#cc0000', // default is blue
	// 		theme        : 'light'    // or dark
	// 	});
	// .then (function (el) {
	// 	// el.contentDocument.querySelector(".footer").style.display = "none";
	// });

	$('[name="tweet"]').each( function() {
		// alert("working");
		var tweet = $(this)[0];
		// console.log(tweet);
		var id = tweet.getAttribute("tweetID");
		// console.log(id);

		twttr.widgets.createTweet(
			id, tweet, 
			{
				conversation : 'none',    // or all
				cards        : 'hidden',  // or visible 
				linkColor    : '#cc0000', // default is blue
				theme        : 'dark'    // or dark
			})
		.then (function (el) {
			// el.contentDocument.querySelector(".footer").style.display = "none";
		});
	});

});