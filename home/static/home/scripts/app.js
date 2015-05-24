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

    .controller('latestController', function($scope){

    })

    .controller('archivesController', function($scope){
	
    })

    .controller('subscribeController', function($scope){

    });
