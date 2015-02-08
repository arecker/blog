// Filter Archives
var filter = function(element){
	var value = $(element).val().toUpperCase();
    var panelLinks = $('.panel p').find('a');
   	panelLinks.each(function() {
        if ($(this).text().toUpperCase().search(value) > -1) {
            $(this).show();
            $(this).next().show();
        } else {
            $(this).hide();
            $(this).next().hide();
        }
    });
};

(function(){

	var vm = {};

	// Email Subscribe
	vm.subscribe = (function(){
		var subscribeVM = {};
		var emailPattern = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		var apiURL = '/api/subscriber/';
		var messages = {
			initial: 'I\'ll send you an email every time I do something new. Don\'t worry - you can unsubscribe at any time.',
			success: 'Most Excellent!  Thanks for signing up',
			already: 'Whaaaat?  You\'re already subscribed, ya dungus.',
			error: 'Crap.  This thing is totally broken.  Try again later.',
			warning: 'Are you sure that\'s right?',
			exception: 'NERDS.  This thing is not working.  Sorry about that.'
		};

		var emailIsValid = function(email){
        	return emailPattern.test(email) && email !== '';
		};

		var beforeSend = function(){
			subscribeVM.waiting = ko.observable(true);
		};

		var afterComplete = function(jqXHR, textStatus){
			vm.waiting = ko.observable(false);
            switch (jqXHR.status) {
                case 201:
                    subscribeVM.successMessage(true);
                    subscribeVM.negativeMessage(false);
                    subscribeVM.message(messages.success);
                    break;
                case 400:
                    subscribeVM.negativeMessage(true);
                    subscribeVM.message(messages.already);
                    break;
                default:
                    subscribeVM.negativeMessage(true);
                    subscribeVM.message(messages.error);
            };
            subscribeVM.badInput(false);
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
	            	full_text: subscribeVM.wantsFullText()
	            }),

	            beforeSend: beforeSend,
	            complete: afterComplete
			});

		};

		return subscribeVM;

	}());

	ko.applyBindings(vm);

}());