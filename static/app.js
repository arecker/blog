$('.main').hide();
var baseURL = "http://api.alexrecker.com/post/"
var Homepage = function(){

	$.getJSON(baseURL, function(data){

		var vm = {
			posts: ko.observableArray(data),
			latest: data[0],
			filter: ko.observable(""),
		}

		vm.latest.date = moment(vm.latest.date).format('MMMM Do YYYY');

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
        return regExp.test(email) && email !== '' && email !== undefined;
	}

	// Properties
	vm.email = ko.observable("");
	vm.wantsFullText = ko.observable(false);
	vm.message = ko.observable("I'll send you an email every time I do something new. Don't worry - you can unsubscribe at any time.");
	vm.badInput = ko.observable(false);
	vm.negativeMessage = ko.observable(false);
	vm.successMessage = ko.observable(false);
	vm.waiting = ko.observable(false);
	
	// Functions
	vm.go = function(){
		var email = vm.email();
		var wantsFullText = vm.wantsFullText();
		var emailIsValid = EmailIsValid(email);
		vm.negativeMessage(false);
		vm.successMessage(false);
		vm.badInput = ko.observable(false);
		if (emailIsValid){

			var key = "";

	        try {
	            key = APP_KEY;
	        } catch(err) {
	            alert('Blurrrrrrrrrrrthis thing is broken try again later.');
	            return;
	        }

	        data = {
	            "email": email,
	            "full_text": wantsFullText
	        }

	        $.ajax({
	            url: 'http://api.alexrecker.com/email/subscriber/add/?app=' + key,
	            type: "POST",
	            dataType: "json",
	            data: JSON.stringify(data),

	            beforeSend: function(){
	                vm.waiting = ko.observable(true);
	            },

	            complete: function (jqXHR, textStatus) {
	            	vm.waitin = ko.observable(false);
	                switch (jqXHR.status) {
	                    case 201:
	                        vm.successMessage(true);
	                        vm.message("Most Excellent!  Thanks for signing up");
	                        break;
	                    case 400:
	                        vm.negativeMessage(true);
	                        vm.message("Whaaaat?  You're already subscribed, ya dungus.");
	                        break;
	                    default:
	                        vm.negativeMessage(true);
	                        vm.message("Crap.  This thing is totally broken.  Try again later.")
	                }
	            }

	        });
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

$('.main').fadeIn(1000);
