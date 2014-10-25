var Application = (function(){

	var baseURL = "http://api.alexrecker.com/post/"
	var Homepage = function(){

		$.getJSON(baseURL, function(data){

			var vm = {
				"posts": data,
				"latest": data[0]
			}

			ko.applyBindings(vm);

		});
	}

	var Postpage = function(slug){

		$.getJSON(baseURL + slug, function(data){

			var vm = {
				"title": data.title,
				"description": data.description,
				"date": moment(data.date).format('MMMM Do YYYY'),
				"body": data.body,
				"link": data.link,
			}

			ko.applyBindings(vm);

		});
	}


	// Routing
	var slug = $('#slug').val();
	var page = undefined;
	switch (slug) {
		case "":
			page = new Homepage();
			break;
		default:
			page = new Postpage(slug);
	}

}());