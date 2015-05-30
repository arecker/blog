(function(angular){

    angular.module('unsubscribe', ['shared'])

        .config(function($httpProvider){
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        });
    
}(angular));
