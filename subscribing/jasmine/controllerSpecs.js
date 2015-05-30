describe('subscribing:controllers', function(){

    beforeEach(module('unsubscribe'));
    
    it('should exist', function(){
        expect(true).toBe(true);
    });

    describe('mainController', function(){
        var $scope;
        
        beforeEach(inject(function($rootScope, $controller){
            $scope = $rootScope.$new();
            $controller('mainController', { $scope: $scope });
        }));

        it('should not intialize with the button disabled', function(){
            expect($scope.disable).toBe(false);
        });

        it('should not initialize showing the email', function(){
            expect($scope.showEmail).toBe(false);
        });
    });
});
