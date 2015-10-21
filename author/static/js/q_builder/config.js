(function() {
    angular.module('QBuilderConfig', [])

        /**
         * Angular application-level configuration
         */

        .config(['$httpProvider', '$provide', function($httpProvider, $provide) {

            /**
             * CSRF Fields
             */
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

            /**
             * Ensure AJAX Headers sent
             */
            $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
        }])
})();
