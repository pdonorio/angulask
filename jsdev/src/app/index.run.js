(function() {
  'use strict';

  angular
    .module('web')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log) {
    $log.debug('test debug');
  }

})();
