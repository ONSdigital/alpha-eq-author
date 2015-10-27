(function() {
  angular.module('tabs', ['QBuilderConfig'])
    .directive('tab', function() {
      return {
        restrict: 'E',
        transclude: true,
        template: '<div ng-show="active" ng-class="{current: active}" ng-transclude></div>',
        require: '^tabset',
        scope: {
          heading: '@'
        },
        link: function(scope, elem, attr, tabsetCtrl) {
          scope.active = false;
          tabsetCtrl.addTab(scope);
        }
      };
    })

  .directive('tabset', function() {
    return {
      restrict: 'E',
      transclude: true,
      scope: {},
      templateUrl: function(element, attrs) {
        return attrs.templateUrl;
      },
      bindToController: true,
      controllerAs: 'tabset',
      controller: function() {
        var self = this;
        self.tabs = [];

        self.addTab = function addtab(tab) {
          self.tabs.push(tab);

          if (self.tabs.length === 1) {
            tab.active = true;
          }
        }

        self.select = function select(selectedTab) {
          angular.forEach(self.tabs, function(tab) {
            if (tab.active && tab !== selectedTab) {
              tab.active = false;
            }
          });

          selectedTab.active = true;
        }
      }
    }
  })
})();
