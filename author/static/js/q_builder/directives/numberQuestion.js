(function() {
  angular.module('numberQuestion', [])

  .directive("numberQuestion", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/number_question.html',
        controller: function($scope) {
            /**
             *  Add an validation rule
             */
            $scope.addValidation = function(question) {

                question.validation.push({
                    condition: '',
                    value: '',
                    type: 'error',
                    message: ''
                });
            };
        },
        controllerAs: 'ctrl'
        };
    });
})();