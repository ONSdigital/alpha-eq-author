(function() {
  angular.module('numberQuestion', [])

  .directive("numberQuestion", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/number_question.html'
        };
    });
})();