(function() {
  angular.module('dateQuestion', [])

  .directive("dateQuestion", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/date_question.html',
        controllerAs: 'ctrl'
        };
    });
})();