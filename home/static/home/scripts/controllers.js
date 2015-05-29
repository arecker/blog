(function(angular){
    angular.module('home')

        .controller('latestController', function($scope, postService){
            postService.fetchLatest().success(function(posts){
                $scope.post = posts[0];
            });
        })

        .controller('archivesController', function($scope, postService){
            postService.fetchArchives().success(function(posts){
                $scope.posts = posts;
	    });
        })

        .controller('subscribeController', function($scope, subscriberService){
            var messageBag = {
                initial: 'I\'ll send you an email every time I do something new. Don\'t worry - you can unsubscribe at any time.',
                redundant: 'Whaaaat?  You\'re already subscribed, ya dungus.',
                success: 'Most Excellent!  Thanks for signing up',
                exception: 'NERDS.  This thing is not working.  Sorry about that.'
            };

            $scope.message = messageBag.initial;
            $scope.alert = 0;
            
            $scope.subscribeFormSubmit = function(){
                var email = $scope.subscriber.email,
                    full = $scope.subscriber.fullText;

                subscriberService.create(email, full)
                    .success(function(){
                        $scope.message = messageBag.success;
                        $scope.alert = 1;
                    })
                    .error(function(data, status){
                        switch(status){
                        case 400:
                            $scope.message = messageBag.redundant;
                            $scope.alert = -1;
                            break;
                        default:
                            $scope.message = messageBag.exception;
                            $scope.alert = -2;
                            break;
                        }
                    });
            };
        })

        .controller('homeNavbarController', function($scope, $location){
            $scope.isActive = function(path){
                return path === $location.path();
            };
        });
    
}(angular));
