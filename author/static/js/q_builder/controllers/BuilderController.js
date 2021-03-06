(function() {
  /**
   *  Main Question Builder controller
   *
   *  Responsible for creating the available question types, and persisting the questionnaire
   */

  angular.module('BuilderController', ['ngAnimate'])
    .controller("BuilderController", function($scope, $http) {

      var startItem = {
        questionText: 'Unnamed Section',
        questionHelp: '',
        questionError: '',
        questionReference: "0",
        questionType: 'QuestionGroup',
        dndType: 'group',
        type: 'group',
        children: [],
        validation: [],
        displayProperties: {},
        displayConditions: [],
        skipConditions: [],
        branchConditions: [],
        parts: []
      };

      $scope.messages = [];
      $scope.models = {
        selected: null,
        section: "0",
        position: 0,
        view: 'single',

        templates: [{
          type: "text_question",
          description: "Text Question",
          id: 1,
          icon: 'fa-font',
          dndType: 'item',
          show: ['open', 'single']
        }, {
          type: "number_question",
          description: "Numeric Question",
          id: 1,
          icon: 'fa-list-ol',
          dndType: 'item',
          show: ['open', 'single']
        }, {
          type: "check_box_question",
          description: "Check Box Question",
          id: 1,
          icon: 'fa-check-square-o',
          dndType: 'item',
          show: ['open', 'single']
        }, {
          type: "radio_question",
          description: "Multiple Choice Single Answer",
          id: 1,
          icon: 'fa-dot-circle-o',
          dndType: 'item',
          show: ['open', 'single']
        }, {
          type: "dropdown_question",
          description: "Dropdown Question",
          id: 1,
          icon: 'fa-caret-square-o-down',
          dndType: 'item',
          show: ['open', 'single']
        }, {
          type: "rich_text_block",
          description: "Rich text field",
          id: 1,
          icon: 'fa-pencil-square-o',
          dndType: 'item',
          show: ['open', 'single']
        }, {
          type: "date_question",
          description: "Date Question",
          id: 1,
          icon: 'fa fa-calendar',
          dndType: 'item',
          show: ['open', 'single']
        }, {
          type: "group",
          /*description: "Section",
          icon: 'fa-th',*/
          id: 1,
          columns: [
            []
          ],
          dndType: 'group',
          show: ['open', 'collapsed']
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
            $scope.models.section = data.questionList[0].questionReference;
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

      $scope.next = function() {
        if ($scope.models.position < $scope.models.dropzones.questionList
          .length - 1) {
          newPosition = $scope.models.position + 1;
          $scope.models.section = $scope.models.dropzones.questionList[
            newPosition].questionReference;
        }
      };

      $scope.previous = function() {
        if ($scope.models.position > 0) {
          newPosition = $scope.models.position - 1;
          $scope.models.section = $scope.models.dropzones.questionList[
            newPosition].questionReference;
        }
      };

      $scope.delete = function(index) {
        $scope.models.dropzones.questionList.splice(index, 1);

        if ($scope.models.dropzones.questionList.length == 0 && $scope.models
          .view == 'single') {
          //if the user deletes the last one, move them to the collapsed view
          $scope.models.section = '0';
          $scope.models.view = 'collapsed'
        } else {
          $scope.models.section = $scope.models.dropzones.questionList[0]
            .questionReference;
        }
      }

      $scope.viewSection = function(section) {
        $scope.models.view = 'single';
        $scope.models.selected = section;
        $scope.models.section = section.questionReference;
      };

      $scope.$watch('models.section', function(model) {
        var questionList = $scope.models.dropzones.questionList;
        $scope.models.position = 0;
        if (questionList.length != 0) {
          for (i = 0; i < questionList.length; i++) {
            var questionGroup = questionList[i];
            if (questionGroup.questionReference == $scope.models.section) {
              $scope.models.position = i;
            }
          }
        }
      }, true);

      $scope.newItem = function(item) {

        question = {
          questionText: '',
          questionHelp: '',
          questionError: '',
          questionReference: '',
          children: [],
          validation: [{
            condition: 'required',
            value: true,
            type: 'error',
            message: 'This field is required'
          }],
          displayProperties: {},
          displayConditions: [],
          skipConditions: [],
          branchConditions: [],
          parts: []
        };

        question.dndType = 'item';

        //add a question reference
        $scope.models.questionnaire_meta.last_used_id += 1;
        question.questionReference = $scope.models.questionnaire_meta.last_used_id
          .toString();

        // FUGLY
        switch (item.type) {
          case 'radio_question':
            question.questionType = 'MultipleChoice';
            question.parts = [{
              type: 'option',
              value: ''
            }];
            question.branchConditions = [{
              jumpTo: {
                question: '',
                condition: {
                  value: {
                    is: ''
                  }
                }
              }
            }];
            break;
          case 'text_question':
            question.questionType = 'InputText';
            question.validation.push({
              condition: 'maxlength',
              value: '',
              type: 'error',
              message: ''
            });
            break;
          case 'dropdown_question':
            question.questionType = 'Dropdown';
            break;
          case 'check_box_question':
            question.questionType = 'CheckBox';
            break;
          case 'number_question':
            question.questionType = 'InputNumber';
            question.validation.unshift({
              condition: 'numeric',
              value: true,
              type: 'error',
              message: 'This field must be numeric'
            });
            //add an empty rule
            question.validation.push({
              condition: '',
              value: '',
              type: 'error',
              message: ''
            });
            break;
          case 'date_question':
            question.questionType = 'Date';
            question.validation.unshift({
              condition: 'date',
              value: true,
              type: 'error',
              message: 'This field must be a date'
            });
            break;
          case 'rich_text_block':
            question.questionType = 'TextBlock';
            break;
          case 'group':
            question.questionType = 'QuestionGroup';
            question.dndType = 'group';
            question.questionText = 'Unnamed Section';
            break;
        }

        // set the type for drag and drop
        question.type = item.type;


        return question;
      }

      $scope.newGroup = function() {
        group = $scope.newItem({
          type: 'group'
        });
        $scope.models.dropzones.questionList.push(group);
        $scope.$digest();
      }

      $scope.$watch('models.dropzones', function(model) {
        $scope.modelAsJson = angular.toJson(model, true);
      }, true);

    });
})();
