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
            var endPoint = '/api/posts/',
                nextPageEndpoint,
                pageSize = 5,
                advancePage = function(url, params){
                    return $http.get(url, params).success(function(data){
                        nextPageEndpoint = data.next;
                    });
                };
            
            return {
                list: function(){
                    return $http.get(endPoint);
                },
                nextPage: function(){
                    if (nextPageEndpoint){
                        return advancePage(nextPageEndpoint);
                    } else {
                        return advancePage(endPoint, {
                            params: { limit: pageSize }
                        });
                    }
                },
                latest: function(){
                    return $http.get(endPoint, {
                        params: { latest: true }
                    });
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
