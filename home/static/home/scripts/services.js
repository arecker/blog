home
    .factory('postService', function($http){
        var postEndpoint = '/api/posts/';
        return {
            'fetchLatest': function(){
                return $http.get(postEndpoint); // TODO: Better viewset to get this
            },
            'fetchArchives': function(){
                return $http.get(postEndpoint);
            }
        };
    });