function Filter(element) {
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
}

var vm = {}

vm.subscribe = (function(){

	var subscribeVM = {}

	function EmailIsValid(email){
        var regExp = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return regExp.test(email) && email !== '' && email !== undefined;
	}

	// Properties
	subscribeVM.email = ko.observable("");
	subscribeVM.wantsFullText = ko.observable(false);
	subscribeVM.message = ko.observable("I'll send you an email every time I do something new. Don't worry - you can unsubscribe at any time.");
	subscribeVM.badInput = ko.observable(false);
	subscribeVM.negativeMessage = ko.observable(false);
	subscribeVM.successMessage = ko.observable(false);
	subscribeVM.waiting = ko.observable(false);

	// Public functions}
	subscribeVM.go = function(){
		var email = subscribeVM.email();
		var wantsFullText = subscribeVM.wantsFullText();
		var emailIsValid = EmailIsValid(email);
		subscribeVM.negativeMessage(false);
		subscribeVM.successMessage(false);
		subscribeVM.badInput = ko.observable(false);
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
	                subscribeVM.waiting = ko.observable(true);
	            },

	            complete: function (jqXHR, textStatus) {
	            	vm.waitin = ko.observable(false);
	                switch (jqXHR.status) {
	                    case 201:
	                        subscribeVM.successMessage(true);
	                        subscribeVM.message("Most Excellent!  Thanks for signing up");
	                        break;
	                    case 400:
	                        subscribeVM.negativeMessage(true);
	                        subscribeVM.message("Whaaaat?  You're already subscribed, ya dungus.");
	                        break;
	                    default:
	                        subscribeVM.negativeMessage(true);
	                        subscribeVM.message("Crap.  This thing is totally broken.  Try again later.")
	                }
	            }
	        });
		} else {
			subscribeVM.badInput(true);
			subscribeVM.negativeMessage(true);
			subscribeVM.message("Are you sure that's right?");
		}
	}
	return subscribeVM;
}());

ko.applyBindings(vm);