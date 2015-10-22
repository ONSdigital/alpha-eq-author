(function() {
  /**
   *  Main Question Builder controller
   *
   *  Responsible for creating the available question types, and persisting the questionnaire
   */

  angular.module('BuilderController', [])
    .controller("BuilderController", function($scope, $http) {
      $scope.messages = [];
      $scope.models = {
        selected: null,

        templates: [{
          type: "text_question",
          description: "Text Question",
          id: 1,
          icon: 'fa-font',
          dndType: 'item'
        }, {
          type: "radio_question",
          description: "Multiple Choice Single Answer",
          id: 1,
          icon: 'fa-dot-circle-o',
          dndType: 'item'
        }, {
          type: "rich_text_block",
          description: "Rich text field",
          id: 1,
          icon: 'fa-pencil-square-o',
          dndType: 'item'
        }, {
          type: "group",
          description: "Question Group",
          icon: 'fa-th',
          id: 1,
          columns: [
            []
          ],
          dndType: 'item'
        }, ],
        dropzones: {
          questionList: []
        }
      };

      // Load the initial questionnaire state
      $http.get(window.location).success(function(data) {
        $scope.models.dropzones.questionList = data.questionList;
        $scope.models.questionnaire_meta = data.meta;
      });

      $scope.saveQuestionnaire = function() {
        $http.post(window.location, {
          'meta': $scope.models.questionnaire_meta,
          'questionList': $scope.models.dropzones.questionList
        }).success(function(data) {
          $scope.messages = [];
          $scope.messages.push(data);
        });
      };

      $scope.dropCallback = function(event, index, item) {
        // check whether we have dropped a new or existing item
        if (!item.hasOwnProperty('questionReference')) {
          return $scope.newItem(item);
        } else {
          return item;
        }
      };

      $scope.newItem = function(item) {

        question = {
          questionText: '',
          questionHelp: '',
          questionError: '',
          questionReference: '',
          children: [],
          validation: {
            required: true
          },
          displayProperties: {},
          displayConditions: [],
          skipConditions: [],
          branchConditions: [],
          parts: []
        };
        // FUGLY
        switch (item.type) {
          case 'radio_question':
            question.questionType = 'MultipleChoice';
            question.parts = [{
              type: 'option',
              value: '',
            }];
            break;
          case 'text_question':
            question.questionType = 'InputText';
            break;
          case 'rich_text_block':
            question.questionType = 'TextBlock';
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
