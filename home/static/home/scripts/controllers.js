home
    .controller('latestController', function($scope, postService){
        postService.fetchLatest().success(function(posts){
			$scope.post = posts[0];
	    });
    })

    .controller('archivesController', function($scope, postService){
	    postService.fetchArchives().success(function(posts){
	        $scope.posts = posts;
	    });
    })

    .controller('subscribeController', function($scope){

    })

    .controller('homeNavbarController', function($scope, $location){
        $scope.isActive = function(path){
            return path === $location.path();
        };
    });