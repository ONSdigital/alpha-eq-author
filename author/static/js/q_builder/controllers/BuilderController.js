(function() {
    /**
     *  Main Question Builder controller
     *
     *  Responsible for creating the available question types, and persisting the questionnaire
     */

    angular.module('BuilderController', [])
        .controller("BuilderController", function($scope, $http) {

            $scope.models = {
                selected: null,

                templates: [
                    {type: "text_question", id: 1, icon: '/static/img/icons/text.svg'},
                    {type: "radio_question", id: 1, icon: '/static/img/icons/radio.svg'},
                    {type: "group", id: 1, columns: [[]]},
                ],
                dropzones: {
                    questionnaire: []
                }
            };

            // Load the initial questionnaire state
            $http.get(window.location).success(function(data) {
                $scope.models.dropzones = data;
            });

            $scope.saveQuestionnaire = function(questionnaire) {
                $http.post(window.location, questionnaire, function(data) {
                    // This needs to be a flash message or something
                    alert('Saved!');
                });
            };

            $scope.dropCallback = function(event, index, item) {
                console.log('Item of type: ' + item.type);

                return $scope.newItem(item);
            };

            $scope.newItem = function(item) {

                // FUGLY
                switch(item.type) {
                    case 'radio_question':
                        item.questionType = 'MultipleChoice';
                        break;
                    case 'text_question':
                        item.questionType = 'InputText';
                        break;
                }

                item.questionText = '';
                item.questionHelp = '';
                item.questionError = '';
                item.questionReference = '';
                item.children = [];
                item.validation = {
                    required: true
                };
                item.displayProperties = {};
                item.displayConditions = [];
                item.skipConditions = [];
                item.branchConditions = [];
                item.parts = [];

                return item;
            }

            $scope.$watch('models.dropzones', function(model) {
                $scope.modelAsJson = angular.toJson(model, true);
            }, true);

        });
})();