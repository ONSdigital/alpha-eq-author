(function() {
  angular.module('radioQuestion', [])

  .directive("radioQuestion", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/radio_question.html',
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

            /**
             *  Add routing rule
             */
            $scope.addRule = function(question) {
                if (typeof question.branchConditions == "undefined" ) {
                    question.branchConditions = [];
                }
                question.branchConditions.push({
                    jumpTo: {
                        question: '',
                        condition: {
                            value : {
                                is : ''
                            }
                        }
                    }
                });
            };
        },
    controllerAs: 'ctrl'
  };

    });
})();