(function(angular){

    angular.module('unsubscribe')

        .controller('mainController', function($scope, unsubscribeService){
            $scope.hitIt = function(){
                unsubscribeService.delete(UNSUBSCRIBE_KEY)
                    .success(function(){
                        alert('gone!');
                    })

                    .error(function(e){
                        console.log(e);
                    });
            };
        });
    
}(angular));
