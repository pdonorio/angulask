(function() {
  'use strict';

  angular
    .module('web')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($scope, $log, $location) {
    $scope.test = 'yes';
    $log.debug("Controller");
    var absUrl = $location.absUrl();
    $log.debug(absUrl)
  }
})();
