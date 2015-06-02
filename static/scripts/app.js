(function(angular){

    angular.module('shared', [])

        .config(function($httpProvider){
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        });
    
}(angular));
