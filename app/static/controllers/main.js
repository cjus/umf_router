/**
 * @name MainCtrl
 * @description Main controller.
 * @author Carlos Justiniano
 */
angular.module('umfTestApp')
  .controller('MainCtrl', ['$scope', '$location', function ($scope, $location) {
    'use strict';

    var VERSION = "1.0"
      , WEBSOCKET_PORT = 5000
      , userID
      , shortUID;

    $scope.payloadSizeOptions = [
      {name: '.5 kB', value: 0.5},
      {name: '1 kB', value: 1},
      {name: '2 kB', value: 2},
      {name: '4 kB', value: 4},
      {name: '8 kB', value: 8},
      {name: '16 kB', value: 16},
      {name: '32 kB', value: 32},
      {name: '64 kB', value: 64},
      {name: '128 kB', value: 128},
      {name: '256 kB', value: 256},
      {name: '512 kB', value: 512},
      {name: '1024 kB', value: 1024}
    ];
    $scope.msgTypes = [
      {name: 'Chat', value: 'chat'},
      {name: 'Client info', value: 'client'},
      {name: 'Mouse position', value: 'mouse'},
      {name: 'Heart beat', value: 'heart'},
      {name: 'Random', value: 'random'}
    ];
    $scope.startTestButtonOptions = [
      {name: 'Start', class: 'btn-primary'},
      {name: 'Stop', class: 'btn-danger'}
    ];
    $scope.iterationChoices = [
      {name: 'One shot', value: 1},
      {name: 'Twice', value: 2},
      {name: 'Five times', value: 5},
      {name: 'Until stopped', value: -1}
    ];
    $scope.console = [];

    $scope.settings = {
      userID: generateUserID(),
      textBuffer: '',
      timerID: null,
      msgPerSecond: 1,
      iterationCnt: 0,
      iteration: $scope.iterationChoices[0],
      payloadSize: $scope.payloadSizeOptions[0],
      msgType: $scope.msgTypes[0],
      startTestButton: $scope.startTestButtonOptions[0]
    };
    userID = $scope.settings.userID;
    $scope.settings.shortUID = userID.slice(0, 2) + userID.slice(userID.length - 2);
    shortUID = $scope.settings.shortUID;

    $scope.messages = [
      {
        "mid": 0,
        "type": "msg",
        "to": "umfTestServer",
        "from": "UMFTester:" + shortUID,
        "version": "1.0",
        "timestamp": "",
        "body": {
        }
      }
    ];

    if ("WebSocket" in window) {
      $scope.ws = new WebSocket("ws://" + document.domain + ":" + WEBSOCKET_PORT + "/ws");
      if ($scope.ws) {
        consoleLog("Initializing UMFTester v" + VERSION);
        consoleLog("Running with userID: " + userID + " (" + shortUID + ")");
        consoleLog("Connected to WebSocket.");
        consoleLog("Ready for testing.");
      }
    }

    $scope.ws.onmessage = function (msg) {
      var message = JSON.parse(msg.data);
      consoleLog("Incoming message: ", message);
    };

    // Cleanly close websocket when unload window
    window.onbeforeunload = function () {
      $scope.ws.onclose = function () {
        // intentionally set to empty
      }; // disable onclose handler first
      $scope.ws.close();
    };

    $scope.startTest = function () {
      var cnt
        , i
        , msg
        , payloadSize
        , settings = $scope.settings;

      settings.startTestButton = (settings.startTestButton.name == 'Start') ?
        $scope.startTestButtonOptions[1] : $scope.startTestButtonOptions[0];

      if (settings.startTestButton.name == 'Start') {
        if (settings.timerID != null) {
          clearInterval($scope.settings.timerID);
          $scope.settings.timerID = null;
          consoleLog("Test ended.");
        }
      } else {
        $scope.console = [];
        payloadSize = settings.payloadSize.value * 1024;
        settings.textBuffer = randomText(payloadSize);
        settings.iterationCnt = Number(settings.iteration.value);

        consoleLog("Starting test.");
        consoleLog("Messages per second: " + settings.msgPerSecond);
        consoleLog("Payload size: " + payloadSize + " bytes.");

        $scope.settings.timerID = setInterval(function () {
          if (settings.iterationCnt == -1) {
            consoleLog("iterationCnt: 1");
          } else {
            consoleLog("iterationCnt: " + settings.iterationCnt);
          }

          var go = true;
          if (settings.iteration.value != -1) {
            if (--settings.iterationCnt < 0) {
              clearInterval($scope.settings.timerID);
              $scope.settings.timerID = null;
              settings.startTestButton = $scope.startTestButtonOptions[0];
              consoleLog("Test ended.");
              go = false;
            }
          }
          if (go) {
            cnt = Number(settings.msgPerSecond);
            for (i = 0; i < cnt; i++) {
              msg = $scope.messages[0];
              msg.body.addon = settings.textBuffer;
              var msgType = $scope.settings.msgType.value;
              if ($scope.settings.msgType.value == "random") {
                msgType = $scope.msgTypes[Math.floor((Math.random() * 4))].value;
              }
              msg = buildUMFMessage(msg, msgType);
              msg = JSON.stringify(msg);
              $scope.ws.send(msg);
            }
          }
          $scope.$apply();
        }, 1000);
      }
    };

    function getDate() {
      var date = new Date()
        , hours = date.getHours()
        , minutes = date.getMinutes()
        , seconds = date.getSeconds();

      hours = hours < 10 ? "0" + hours : hours;
      minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      return "" + hours + ":" + minutes + ":" + seconds + "." +
        date.getMilliseconds();
    }

    function consoleLog(message, objectValue) {
      var strDate = getDate();
      try {
        if (typeof objectValue != "undefined") {
          if (typeof objectValue == "object") {
            message = message + "(object) " + JSON.stringify(objectValue);
          } else {
            message = message + "(" + typeof message + ") " + objectValue;
          }
        }

        $scope.console.push(strDate + " | (" + $scope.settings.shortUID + "): " + message);
      } catch (exception) {
      }
    }

    function randomText(count) {
      var chars = "ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz"
        , buffer = ''
        , i
        , rnum
        , wordSpace;

      for (i = 0; i < count; i++) {
        wordSpace = Math.floor(Math.random() * 5) + 2;
        if (count % wordSpace) {
          buffer += ' ';
        }
        rnum = Math.floor(Math.random() * chars.length);
        buffer += chars.substring(rnum, rnum + 1);
      }
      return buffer;
    }

    function generateUserID() {
      var strDate = getDate();
      return Sha1.hash(strDate);
    }

    function buildUMFMessage(message, messageType) {
      var dateUTC = new Date().toUTCString()
        , iso8601TimeStamp = new Date(dateUTC).toISOString();
      message.type = messageType;
      message.timestamp = iso8601TimeStamp;
      message.mid = UUID.generateWeakUUID();
      return message;
    }

  }]);
