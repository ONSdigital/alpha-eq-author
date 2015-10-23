(function() {
  angular.module('richTextQuestion', [])

  .directive("richTextQuestion", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/rich_text_question.html'
        };
    });
})();