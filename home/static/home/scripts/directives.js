(function(angular){

    angular.module('home')

        .directive('homeNavbar', function(){
            return {
                restrict: 'E',
                controller: 'homeNavbarController',
                templateUrl: '/static/home/scripts/homeNavbar.html'
            }
        });
    
}(angular));
