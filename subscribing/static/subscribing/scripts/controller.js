(function(angular){

    angular.module('unsubscribe')

        .controller('mainController', function($scope, subscriberService){
            $scope.showEmail = false;
            $scope.disable = false;
            $scope.hitIt = function(){
                subscriberService.delete(UNSUBSCRIBE_KEY)
                    .success(function(){
                        $scope.message = 'Alrighty - you\'re all done with me.  I\'ll miss you!';
                        $scope.disable = true;
                    })

                    .error(function(e){
                        $scope.message = 'Crap.  Something went wrong.  Try to unsubscribe later, or just send me an email';
                        $scope.showEmail = true;
                    });
            };
        });
    
}(angular));
