
var baseURL = "http://api.alexrecker.com/post/"
var Homepage = function(){

	$.getJSON(baseURL, function(data){

		var vm = {
			"posts": ko.observableArray(data),
			"latest": data[0],
			filter: ko.observable(""),
		}

		vm.filteredPosts = ko.computed(function() {
		    var filter = this.filter().toLowerCase();
		    if (!filter) {
		        return this.posts();
		    } else {
		        return ko.utils.arrayFilter(this.posts(), function(item) {
		            return item.title.toLowerCase().indexOf(filter) !== -1 ||
		            	   item.description.toLowerCase().indexOf(filter) !== -1;
		        });
		    }
		}, vm);

		vm.subscribe = SubscribeApp;

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

		vm.subscribe = SubscribeApp;

		ko.applyBindings(vm);

	});
}


var SubscribeApp = (function(){
	var vm = {};

	function EmailIsValid(email){
        var regExp = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return regExp.test(self.email) && self.email != '';
	}

	// Properties
	vm.email = ko.observable("");
	vm.wantsFullText = ko.observable(false);
	vm.message = ko.observable("I'll send you an email every time I do something new. Don't worry - you can unsubscribe at any time.");
	vm.badInput = ko.observable(false);
	vm.negativeMessage = ko.observable(false);
	
	// Functions
	vm.go = function(){
		var email = vm.email();
		var wantsFullText = vm.wantsFullText();
		var emailIsValid = EmailIsValid(email);
		if (emailIsValid){
			// go
		} else {
			vm.badInput(true);
			vm.negativeMessage(true);
			vm.message("Are you sure that's right?");
		}
	}

	return vm;
}())


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
