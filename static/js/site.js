(function(){

	var vm = {};

	// Archive Filtering
	vm.ArchiveSearch = {
		query: ko.observable(''),
		filter: function(){
			var query = this.query().toUpperCase();
		}
	};

	// Email Subscribe
	vm.EmailSubscribe = (function(){
		var subscribeVM = {};
		var emailPattern = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		var apiURL = '[ url here ]';
		var messages = {
			initial: 'I\'ll send you an email every time I do something new. Don\'t worry - you can unsubscribe at any time.',
			success: 'Most Excellent!  Thanks for signing up',
			already: 'Whaaaat?  You\'re already subscribed, ya dungus.',
			error: 'Crap.  This thing is totally broken.  Try again later.',
			warning: 'Are you sure that\'s right?'
		};

		var emailIsValid = function(email){
        	return emailPattern.test(email) && email !== '';
		};

		subscribeVM.email = ko.observable("");
		subscribeVM.wantsFullText = ko.observable(false);
		subscribeVM.message = ko.observable(messages.initial);
		subscribeVM.badInput = ko.observable(false);
		subscribeVM.negativeMessage = ko.observable(false);
		subscribeVM.successMessage = ko.observable(false);
		subscribeVM.waiting = ko.observable(false);

		subscribeVM.go = function(){
			var inputEmail = subscribeVM.email();
			
			if (!emailIsValid(inputEmail)){
				subscribeVM.badInput(true);
				subscribeVM.negativeMessage(true);
				subscribeVM.message(messages.warning);
				return;
			};

			$.ajax({
				url: apiURL,
				type: 'POST',
				dataType: "json",
	            data: JSON.stringify({
	            	email: inputEmail,
	            	full_text: subscribeVM.wantsFullText();
	            }),
			});

		};

	}());

	ko.applyBindings(vm);

}());