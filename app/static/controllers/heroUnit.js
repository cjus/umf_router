'use strict';

/**
 * @name HerounitCtrl
 * @description Hero Unit controller
 * @author Carlos Justiniano
 */
angular.module('umfTestApp')
  .controller('HerounitCtrl', ['$scope', '$location', function ($scope, $location) {
    $scope.showHeroUnit = true;
    $scope.closeHeroUnit = function () {
      this.showHeroUnit = false;
    };
    $scope.learnMore = function () {
      $location.path("/learnmore");
    };
  }]);
