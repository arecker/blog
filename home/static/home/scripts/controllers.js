(function(angular){
    angular.module('home').controller('latestController', function($scope, postService){
        postService.fetchLatest().success(function(posts){
			$scope.post = posts[0];
	    });
    }).controller('archivesController', function($scope, postService){
        postService.fetchArchives().success(function(posts){
	        $scope.posts = posts;
	    });
    }).controller('subscribeController', function($scope){
        $scope.subscribeFormSubmit = function(){
            var email = $scope.subscriber.email,
                full = $scope.subscriber.fullText;
            alert('Email: ' + email + '\nFullText: ' + full);
        };
    }).controller('homeNavbarController', function($scope, $location){
        $scope.isActive = function(path){
            return path === $location.path();
        };
    });
}(angular));