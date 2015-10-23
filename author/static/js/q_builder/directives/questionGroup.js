(function() {
  angular.module('questionGroup', [])

  .directive("questionGroup", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/question_group.html'
        };
    });
})();