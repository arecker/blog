(function(angular){

    angular.module('unsubscribe')

        .factory('unsubscribeService', function($http){
            return {
                delete: function(key){
                    var endPoint = '/api/subscribers/';
                    return $http.delete(endPoint + key);
                }
            };
        });
    
}(angular));
