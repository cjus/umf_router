'use strict';

/**
 * @name umfTesterApp
 * @description  umfTesterApp module. Includes dependency loading and router.
 * @author Carlos Justiniano
 */
angular.module('umfTestApp', [])
  .config(function ($routeProvider, $locationProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/learnmore', {
        templateUrl: 'views/learnmore.html',
        controller: 'LearnmoreCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
    $locationProvider.html5Mode(true);
  });
