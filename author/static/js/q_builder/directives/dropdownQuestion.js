(function() {
  angular.module('dropdownQuestion', [])

  .directive("dropdownQuestion", function() {
    return {
        restrict: 'E',
        templateUrl: '/static/js/q_builder/templates/dropdown_question.html',
        controller: function($scope, $http) {

        /**
         *  load available json list imports into the ui dropdown
         */

        $http.get('/static/js/q_builder/json/jsonImportList.json').
        success(function(data) {
            $scope.jsonImportList = data;
        });

        /**
         *  load the json list into the questionnaire json
         */

        $scope.load = function(jsonImport,question) {

            if (jsonImport != null){
                $http.get('/static/js/q_builder/json/' + jsonImport +'.json').
                    success(function(data) {
                        angular.element('.status').addClass('success');
                        question.parts = [];

                        for (var key in data.elements){
                            question.parts.push({
                            type: 'option',
                            value: data.elements[key].value
                            });
                        }
                    });
                };
            };
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


