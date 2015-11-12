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
        section: "0",
        position: 1,
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
          icon: 'fa-dot-circle-o',
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
            $scope.models.section = data.questionList[0].questionReference.toString();
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
          .length) {
          $scope.models.position = $scope.models.position + 1;
          $scope.models.section = $scope.models.dropzones.questionList[
            $scope.models.position - 1].questionReference;
        }
      };

      $scope.previous = function() {
        if ($scope.models.position > 0) {
          $scope.models.position = $scope.models.position - 1;
          //position in the array is 1 less than the position recorded (we started at 1)
          $scope.models.section = $scope.models.dropzones.questionList[
            $scope.models.position - 1].questionReference;
        }
      };


      $scope.viewSection = function(section) {
        $scope.models.view = 'single';
        $scope.models.selected = section;
        $scope.models.section = section.questionReference.toString();
      };

      $scope.$watch('models.section', function(model) {
        var questionList = $scope.models.dropzones.questionList;
        $scope.models.position = 0;
        if (questionList.length != 0) {
          for (i = 0; i < questionList.length; i++) {
            var questionGroup = questionList[i];
            if (questionGroup.questionReference == $scope.models.section) {
              $scope.models.position = i + 1;
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

        //add a question reference
        $scope.models.questionnaire_meta.last_used_id += 1;
        question.questionReference = $scope.models.questionnaire_meta.last_used_id.toString();

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
                        value : {
                            is : ''
                        }
                    }
                 }
            }];
            break;
          case 'text_question':
            question.questionType = 'InputText';
            break;
          case 'dropdown_question':
            question.questionType = 'Dropdown';
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
        $scope.models.dropzones.questionList.unshift(group);
        $scope.$digest();
      }

      $scope.$watch('models.dropzones', function(model) {
        $scope.modelAsJson = angular.toJson(model, true);
      }, true);

    });
})();
