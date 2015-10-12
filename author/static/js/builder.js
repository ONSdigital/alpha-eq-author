(function() {
/**
 * The controller doesn't do much more than setting the initial data model
 */
angular.module("builder", ['dndLists'])
.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
}])
.controller("BuilderController", function($scope, $http) {

    $scope.models = {
        selected: null,

        templates: [
            {type: "text_question", id: 1, icon: '/static/img/icons/text.svg'},
            {type: "radio_question", id: 1, icon: '/static/img/icons/radio.svg'},
            {type: "new_question_type", id: 1, icon: '/static/img/icons/grid.svg'},
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
            alert('Saved!');
        });
    };

    $scope.$watch('models.dropzones', function(model) {
        $scope.modelAsJson = angular.toJson(model, true);
    }, true);

})
.controller('RadioQuestionController', function($scope) {
    $scope.addOption = function(question) {
        if (typeof question.answers == "undefined" ) {
            question.answers = [];
        }
        question.answers.push({ value: '' });
    };
})
})();