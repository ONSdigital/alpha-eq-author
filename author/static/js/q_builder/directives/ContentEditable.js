(function() {
  angular.module('contenteditable', [])
    .directive("contenteditable", function() {
      return {
        restrict: "A",
        require: "ngModel",
        link: function(scope, element, attrs, ngModel) {

          function read() {
            ngModel.$setViewValue(element.text());
          }

          ngModel.$render = function() {
            // Do not allow drag and drop into contenteditable
            element.attr("ondragenter",
              "event.preventDefault(); event.dataTransfer.dropEffect = 'none'"
            );
            element.attr("ondragover",
              "event.preventDefault(); event.dataTransfer.dropEffect = 'none'"
            );
            element.html(ngModel.$viewValue || "");
          };

          element.bind("blur keyup change", function() {
            scope.$apply(read);
          });
        }
      };
    });
})();
