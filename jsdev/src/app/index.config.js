(function() {
  'use strict';

  angular
    .module('web')
    .config(config);

  function config($logProvider) {
    // Enable log
    $logProvider.debugEnabled(true);
  }

})();
