describe('home:controllers', function(){

    beforeEach(module('home'));
    
    it('should exist', function(){
        expect(true).toBe(true);
    });

    describe('subscribeController', function(){

        var $scope, mockSubscriberService;

        beforeEach(inject(function($rootScope, $controller){
            $scope = $rootScope.$new();
            $controller('subscribeController', { $scope: $scope });
        }));
        

        it('should be initialized with the correct message', function(){
            var expected = 'I\'ll send you an email every time I do something new. Don\'t worry - you can unsubscribe at any time.',
                actual = $scope.message;
            expect(actual).toBe(expected);
        });

        // it('should pass the email and full text setting to the service', function(){
        //     $scope.subscriber = {};
        //     $scope.subscriber.email = 'test@email.com';
        //     $scope.subscriber.fullText = true;

        //     $scope.subscribeFormSubmit();
        // });
        
    });
});
