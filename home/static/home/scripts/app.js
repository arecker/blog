(function(){
    angular.module('home', ['ngRoute']).config(function($routeProvider){
        $routeProvider.when('/', {
            templateUrl: '/static/home/views/latest.html',
            controller: 'latestController'
        }).when('/archives', {
            templateUrl: '/static/home/views/archives.html',
            controller: 'archivesController'
        }).when('/subscribe', {
            templateUrl: '/static/home/views/subscribe.html',
            controller: 'subscribeController'
        });
    });
}());