(function(angular){
    angular.module('home')

        .factory('postService', function($http){
            var postEndpoint = '/api/posts/';
            return {
                'fetchLatest': function(){
                    return $http.get(postEndpoint + '?latest=true');
                },
                'fetchArchives': function(){
                    return $http.get(postEndpoint);
                }
            };
        });
    
}(angular));
