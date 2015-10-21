(function() {
  angular.module('wysiwygEditor', [])
    .directive('wysiwygEditor', function($timeout) {
      return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModel) {
          // Start the editor
          Simditor.locale = 'en_US';
          toolbar = ['bold', 'italic', 'underline', 'ol', 'ul'];
          element.editor = new Simditor({
            textarea: $(element),
            toolbar: toolbar
          });

          element.editor.on('valuechanged', function(e) {
            $timeout(function() {
              ngModel.$setViewValue(element.editor.getValue());
            });
          });

          ngModel.$render = function() {
            element.editor.setValue(ngModel.$viewValue).trigger(
              'change');
          }
        }
      };
    });
})();
