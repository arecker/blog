var Blog = angular.module('Blog', []);

Blog.factory('apiService', function($http){
	var subscribeEndpoint = '/api/subscribing/subscribe/';
	var postEndpoint = '/api/blogging/post/';
	return {
		createSubscriber: function(data){
			return $http.post(subscribeEndpoint, data);
		},
		fetchArchives: function(){
			return $http.get(postEndpoint);
		}
	};
});

Blog.controller('SubscribeController', function($scope, apiService){
	var messageBag = {
		initial: 'I\'ll send you an email every time I do something new. Don\'t worry - you can unsubscribe at any time.',
		redundant: 'Whaaaat?  You\'re already subscribed, ya dungus.',
		success: 'Most Excellent!  Thanks for signing up',
		exception: 'NERDS.  This thing is not working.  Sorry about that.'
	};

	$scope.message = messageBag.initial;
	$scope.fullText = false;

	$scope.submit = function(){
		var data = {
			email: $scope.email,
			full_text: $scope.fullText
		};

		apiService.createSubscriber(data).success(function(data, status, headers, config){
				$scope.message = messageBag.success;
		}).error(function(data, status, headers, config){
			switch (status) {
				case 400:
					$scope.message = messageBag.redundant;
					break;
				default:
					$scope.message = messageBag.exception;
					break;
			};
		});
	};

});

Blog.controller('ArchivesController', function($scope, apiService){
	apiService.fetchArchives().success(function(data, status, headers, config){
			$scope.posts = data;
	});
});