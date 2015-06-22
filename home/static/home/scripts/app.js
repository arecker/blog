(function(angular){
    angular.module('home', ['ngRoute', 'shared'])
    
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
                })

                .when('/projects', {
                    templateUrl: '/static/home/views/projects.html',
                    controller: 'projectsController'
                });
            
        });
    
}(angular));
