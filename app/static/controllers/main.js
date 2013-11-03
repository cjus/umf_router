'use strict';

/**
 * @name MainCtrl
 * @description Main controller.
 * @author Carlos Justiniano
 */
angular.module('umfTestApp')
  .controller('MainCtrl', ['$scope', '$location', function ($scope, $location) {
    if ("WebSocket" in window) {
      $scope.ws = new WebSocket("ws://" + document.domain + ":5000/ws");

      $scope.ws.onmessage = function (msg) {
        var message = JSON.parse(msg.data);
        console.log("message: " + message.output);
        //$("p#log").html(message.output);
      };
    }

    $scope.sendData = function () {
      $scope.ws.send(JSON.stringify({'output': 'Sent from my browser!'}));
    };

    // Cleanly close websocket when unload window
    window.onbeforeunload = function () {
      $scope.ws.onclose = function () {
      }; // disable onclose handler first
      $scope.ws.close()
    };

  }]);
