(function(angular){

    angular.module('unsubscribe', [])

        .config(function($httpProvider){
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        });
    
}(angular));
