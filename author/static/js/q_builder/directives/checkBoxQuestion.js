(function() {
  angular.module('checkBoxQuestion', [])

  .directive("checkBoxQuestion", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/check_box_question.html',
        controller: function($scope) {

            /**
             *  Add an answer option
             */
            $scope.addOption = function(question) {
                if (typeof question.parts == "undefined" ) {
                    question.parts = [];
                }
                question.parts.push({
                    type: 'option',
                    value: ''
                });
            };
        },
    controllerAs: 'ctrl'
  };

    });
})();