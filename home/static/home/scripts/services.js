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
        })

	.factory('subscriberService', function($http){
            var subscriberEndpoint = '/api/subscribers/';
            return {
                create: function(email, fullText){
                    return $http.post(subscriberEndpoint, {
                        'email': email,
                        'full_text': fullText
                    });
                }
            };
        });
    
}(angular));
