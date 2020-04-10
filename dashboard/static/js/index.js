$(function() {
	var $frame = $("#Frame").first();
	var $photo = $("#Photo").first();
	var $time = $("#Time").first();

	$photo.bind("load", function() {
	});

	UpdateClock();
	NextImage();

	function NextImage() {
		$.ajax({url: "/gallery/next", success: function(result){
			console.log('Next image: ' + result.path);
	        $photo.attr("src", result.path);
	    }});
	    setTimeout(NextImage, 5 * 60 * 1000);
	}

	function UpdateClock() {
		$time.text(moment().format("hh:mm"));
		setTimeout(UpdateClock, 60 * 1000);
	}
});