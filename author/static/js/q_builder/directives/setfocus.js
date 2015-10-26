(function() {
  angular.module('setfocus', [])

  .directive('setfocus', function() {
    return {
      scope: {
        setfocus: '='
      },
      link: function(scope, element) {
        if (scope.setfocus) element[0].focus();
      }
    };
  });
})();
