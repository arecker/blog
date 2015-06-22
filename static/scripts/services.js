(function(angular){

    angular.module('shared')

        .factory('subscriberService', function($http){
            var endPoint = '/api/subscribers/';
            return {
                create: function(email, fullText){
                    return $http.post(endPoint, {
                        'email': email,
                        'full_text': fullText
                    });
                },
                delete: function(key){
                    return $http.delete(endPoint + key + '/');
                }
            };
        })

        .factory('postService', function($http){
            var endPoint = '/api/posts/';
            return {
                list: function(){
                    return $http.get(endPoint);
                },
                latest: function(){
                    return $http.get(endPoint + '?latest=true');
                }
            };
        })

        .factory('projectService', function($http){
            var endPoint = '/api/projects/';
            return {
                list: function(){
                    return $http.get(endPoint);
                }
            };
        });
    
}(angular));
