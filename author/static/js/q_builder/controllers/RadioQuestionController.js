(function() {
    angular.module('RadioQuestionController', [])

        /**
         *  Controller to handle Radio Button Question Types
         *
         */

        .controller('RadioQuestionController', function($scope) {

            /**
             *  Add an answer option
             */
            $scope.addOption = function(question) {
                if (typeof question.parts == "undefined" ) {
                    question.parts = [];
                }
                question.parts.push({
                    type: 'option',
                    name: '',
                    label: '',
                    value: ''
                });
            };
        })
})();