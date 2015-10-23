(function() {
  angular.module('textQuestion', [])

  .directive("textQuestion", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/text_question.html'
        };
    });
})();