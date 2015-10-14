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
                    {type: "text_question", id: 1, icon: '/static/img/icons/text.svg', dndType:'item'},
                    {type: "radio_question", id: 1, icon: '/static/img/icons/radio.svg', dndType:'item'},
                    {type: "group", id: 1, columns: [[]], dndType: 'item'},
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
                // check whether we have dropped a new or existing item
                if ( ! item.hasOwnProperty('questionReference')) {
                    return $scope.newItem(item);
                } else {
                    return item;
                }
            };

            $scope.newItem = function(item) {

                question = {
                    questionText : '',
                    questionHelp : '',
                    questionError : '',
                    questionReference : '',
                    children : [],
                    validation : {
                        required: true
                    },
                    displayProperties : {},
                    displayConditions : [],
                    skipConditions : [],
                    branchConditions : [],
                    parts : []
                };
                // FUGLY
                switch(item.type) {
                    case 'radio_question':
                        question.questionType = 'MultipleChoice';
                        break;
                    case 'text_question':
                        question.questionType = 'InputText';
                        break;
                }

                // set the type for drag and drop
                question.type = item.type;
                question.dndType = 'item';

                return question;
            }

            $scope.$watch('models.dropzones', function(model) {
                $scope.modelAsJson = angular.toJson(model, true);
            }, true);

        });
})();