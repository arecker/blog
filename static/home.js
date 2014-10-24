
$(document).ready(function(){
	var urlRoot = "http://api.alexrecker.com/";
	$.getJSON(urlRoot + "post/", function(data){
		var somethings = data;
		var ViewModel = {
			posts: somethings,
			latest: somethings[0]
		}

		ko.applyBindings(ViewModel);
	});
});