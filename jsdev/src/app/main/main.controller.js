(function() {
  'use strict';

  angular
    .module('web')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($scope, $log, $location) {
    $scope.test = 'yes';
/*
    $log.debug("Controller");
    console.log($location);
    var absUrl = $location.absUrl();
    $log.debug($location.$$url);
*/
    var routes = $location.$$url.split('/');
    $log.debug(routes);
    for (var i = 0; i < routes.length; i++) {
      if (routes[i] == "angular")
        $scope.first = "active";
      else if (routes[i] == "new")
        $scope.second = "active";
    };

    // FIRST LEVEL
    if ($scope.first) {
      $log.info("First");
    }
    // SECOND LEVEL
    if ($scope.second) {
      $log.info("Second");
    }
  }
})();
