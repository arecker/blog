describe('home:controllers', function(){

    beforeEach(module('home'));
    
    it('should exist', function(){
        expect(true).toBe(true);
    });

    describe('subscribeController', function(){

        var $scope;

        beforeEach(function () {

            var mockSubscriberService = function(){
                this.create = function(email, fullText){
                    this._email = email;
                    this._fullText = fullText;

                    return {
                        success: function(){
                            return {
                                error: function(){}
                            };
                        }
                    };
                };
            };

            module(function ($provide) {
                $provide.value('subscriberService', new mockSubscriberService());
            });

        });

        beforeEach(inject(function($rootScope, $controller){
            $scope = $rootScope.$new();
            $controller('subscribeController', { $scope: $scope });
        }));
        

        it('should be initialized with the correct message', function(){
            var expected = 'I\'ll send you an email every time I do something new. Don\'t worry - you can unsubscribe at any time.',
                actual = $scope.message;
            expect(actual).toBe(expected);
        });

        it('should pass the email and full text setting to the service', inject(function(subscriberService){
            $scope.subscriber = {};
            $scope.subscriber.email = 'test@email.com';
            $scope.subscriber.fullText = true;

            $scope.subscribeFormSubmit();

            expect(subscriberService._email).toBe('test@email.com');
            expect(subscriberService._fullText).toBe(true);
        }));
        
    });
});
