(function() {
  angular.module('questionGroup', [])

  .directive("questionGroup", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/question_group.html',
         controller: function($scope) {

            /**
             *  Clear unnamed section title
             */
            $scope.initSection = function(item) {

               if (item.questionText =='Unnamed Section'){
                item.questionText ='';
                }
            };

             /**
             *  insert placeholder if empty
             */
               $scope.emptyHeader = function(item) {
               if (item.questionText ==''){
                item.questionText ='Unnamed Section';
                }
            };
        },
        controllerAs: 'ctrl'
        };
    });
})();