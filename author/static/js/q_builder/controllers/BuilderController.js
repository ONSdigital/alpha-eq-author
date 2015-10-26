(function() {
  /**
   *  Main Question Builder controller
   *
   *  Responsible for creating the available question types, and persisting the questionnaire
   */

  angular.module('BuilderController', [])
    .controller("BuilderController", function($scope, $http) {

      var startItem = {
          questionText: '',
          questionHelp: '',
          questionError: '',
          questionReference: 'start',
          questionType: 'QuestionGroup',
          dndType: 'group',
          type: 'group',
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
          type: "number_question",
          description: "Numeric Question",
          id: 1,
          icon: 'fa-list-ol',
          dndType: 'item'
        }, {
          type: "check_box_question",
          description: "Check Box Question",
          id: 1,
          icon: 'fa-check-square-o',
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
          dndType: 'group'
        }, ],
        dropzones: {
           questionList: []
        }
      };

      // Load the initial questionnaire state
      $http.get(window.location).success(function(data) {
        if (data.locked) {
          $scope.messages = [];
          $scope.messages.push(data);
        } else {
          if (data.questionList.length != 0) {
           $scope.models.dropzones.questionList = data.questionList;
          } else {
            $scope.models.dropzones.questionList = [startItem];
          }
         $scope.models.questionnaire_meta = data.meta;
        }
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

      $scope.endEdit = function() {
        $http.post(window.location, {
          'unlock': 'true'
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

        question.dndType = 'item';

        // FUGLY
        switch (item.type) {
          case 'radio_question':
            question.questionType = 'MultipleChoice';
            question.parts = [{
              type: 'option',
              value: ''
            }];
            break;
          case 'text_question':
            question.questionType = 'InputText';
            break;
          case 'check_box_question':
            question.questionType = 'CheckBox';
            break;
          case 'number_question':
            question.questionType = 'InputText';
            question.validation["numeric"] = true;
            break;
          case 'rich_text_block':
            question.questionType = 'TextBlock';
            break;
          case 'group':
            question.questionType = 'QuestionGroup';
            question.dndType = 'group';
            break;
        }

        // set the type for drag and drop
        question.type = item.type;


        return question;
      }

      $scope.$watch('models.dropzones', function(model) {
        $scope.modelAsJson = angular.toJson(model, true);
      }, true);

    });
})();
