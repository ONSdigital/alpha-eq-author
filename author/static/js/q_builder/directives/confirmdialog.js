(function() {
  angular.module("confirmdialog", [])
    .directive('ngConfirmClick', function() {
      console.log('ngConfirmClick loaded');
      return {
        priority: -1,
        restrict: 'A',
        link: function(scope, element, attrs) {
          console.log('ngConfirmClick linked');
          element.bind('click', function(e) {
            console.log('Attempting to kill kitten');
            var message = attrs.ngConfirmClick;
            if (message && !confirm(message)) {
              e.stopImmediatePropagation();
              e.preventDefault();
            }
          });
        }
      }
    });
})();
