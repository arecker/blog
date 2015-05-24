angular.module('blog', ['ngRoute'])
    .config(function($routeProvider){
	    $routeProvider
            .when('/', {
                templateUrl: '/static/home/views/latest.html',
                controller: 'latestController'
            })

            .when('/archives', {
                templateUrl: '/static/home/views/archives.html',
                controller: 'archivesController'
            })

            .when('/subscribe', {
                templateUrl: '/static/home/views/subscribe.html',
                controller: 'subscribeController'
            });
        })

    .factory('postService', function($http){
        var postEndpoint = '/api/posts/';
        return {
            'fetchLatest': function(){
                return $http.get(postEndpoint); // TODO: Better viewset to get this
            },
            'fetchArchives': function(){
                return $http.get(postEndpoint);
            }
        };
    })

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
