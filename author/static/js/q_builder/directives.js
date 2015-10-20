(function() {
    angular.module('contenteditable', [])
        .directive("contenteditable", function() {
          return {
            restrict: "A",
            require: "ngModel",
            link: function(scope, element, attrs, ngModel) {

              function read() {
                ngModel.$setViewValue(element.html());
              }

              ngModel.$render = function() {
                // Do not allow drag and drop into contenteditable
                element.attr("ondragenter", "event.preventDefault(); event.dataTransfer.dropEffect = 'none'");
                element.attr("ondragover", "event.preventDefault(); event.dataTransfer.dropEffect = 'none'");
                element.html(ngModel.$viewValue || "");
              };

              element.bind("blur keyup change", function() {
                scope.$apply(read);
              });
            }
          };
        });

    angular.module('wysiwygEditor', [])
        .directive('wysiwygEditor', function($timeout) {
          return {
            restrict: 'A',
            require: 'ngModel',
            link: function(scope, element, attrs, ngModel) {
              // Start the editor
              Simditor.locale = 'en_US';
              element.editor = new Simditor({
                textarea: $(element)
              });

              element.editor.on('valuechanged', function(e) {
                  $timeout(function() {
                    ngModel.$setViewValue(element.editor.getValue());
                  });
              });

              ngModel.$render = function() {
                element.editor.setValue(ngModel.$viewValue).trigger('change');
              }
            }
          };
        });
})();
