var ViewModel = {
	"archives": [],
	"latest": undefined,
}

var RequestFactory = function(urlAfterSlash, bindTarget){
	var urlRoot = "http://api.alexrecker.com/";
	$.getJSON(urlRoot + bindTarget, function(data){
		bindTarget = data
	});
}

RequestFactory('', ViewModel.archives);
ViewModel.latest = ViewModel.archives[0];

ko.applyBindings(ViewModel);