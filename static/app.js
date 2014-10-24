var App = function(slug) {
	slug = slug || "";
	var self = this;
	self.go = function(){
		$.getJSON('http://api.alexrecker.com/post/' + slug, function(data){
			var vm = {}
			if (slug === undefined || slug === ""){
				vm.posts = data;
				vm.latest = vm.posts[0];
			} else {
				
			}

			ko.applyBindings(vm);
		});
	}
}


var App = new App();
App.go();