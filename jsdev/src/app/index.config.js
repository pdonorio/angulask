(function() {
  'use strict';

angular.module('web').config(config);

function config($logProvider, $locationProvider) {
	// Enable log
	$logProvider.debugEnabled(true);
	// HTML5 mode: remove hash bang to let url be parsable
	$locationProvider.html5Mode(true);

}

})();
