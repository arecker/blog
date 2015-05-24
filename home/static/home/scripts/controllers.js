home
    .controller('latestController', function($scope, postService){
        postService.fetchLatest().success(function(response){
			$scope.post = response.results[0];
	    });
    })

    .controller('archivesController', function($scope, postService){
	    postService.fetchArchives().success(function(response){
	        $scope.posts = response.results;
	    });
    })

    .controller('subscribeController', function($scope){

    })

    .controller('homeNavbarController', function($scope, $location){
        $scope.isActive = function(path){
            return path === $location.path();
        };
    });