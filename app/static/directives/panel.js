/**
 * @name  panel
 * @description  Panel Directive.  Implements <panel> which
 *  displays a rounded panel with various effects.
 * @author Carlos Justiniano
 */
angular.module('umfTestApp')
  .directive('panel', function() {
    'use strict';
    var defaults = {
      panelBorderStyle: 'solid 1px #ECECEC', /* styling for panel border */
      panelMargin: '0 0 12px 0', /* margin around panel */
      panelBackgroundColor: '#FFFFFF', /* panel background color */
      panelTextColor: '#d3d3d3', /* panel text color */
      panelOpen: true, /* panel initially open (true) or closed (false) */
      panelShadowEnabled: true, /* enable or disable panel shadow */
      panelSlideSpeed: 400, /* panel animation speed */
      borderRadius: '.5em', /* border radius */
      panelTitleBorderStyle: 'solid 1px #BABABA', /* panel title boarder style */
      panelTitleShadeStart: '#D1D1D1', /* Panel title start gradient color */
      panelTitleShadeEnd: '#BABABA', /* Panel title end gradient color */
      panelTitleFontFamily: 'Helvetica, sans-serif', /* Panel title font */
      panelTitleFontSize: '16px', /* default panel title font size */
      panelTitleFontWeight: 'bold', /* default panel title font weight */
      panelTitleColor: '#333333' /* default css color for panel title text */
    };
    var options = angular.extend(defaults, options);
    return {
      template: '<div class="panel">' +
        '<div class="panel-title">{{ title }}</div>' +
        '<div class="panel-content"><div ng-transclude></div></div>' +
        '</div>',
      restrict: 'E',
      transclude: true,
      scope: {
        title: '=',
        minititle: '='
      },
      link: function postLink(scope, element, attrs) {
        var panel = element.find('.panel');
        panel.css({
          'margin': options.panelMargin,
          '-moz-border-radius': options.borderRadius,
          '-webkit-border-radius': options.borderRadius,
          'border-radius': options.borderRadius,
          'border': options.panelBorderStyle,
          'background': options.panelBackgroundColor,
          'color': options.panelTextColor
        });

        if (options.panelShadowEnabled) {
          panel.css({
            '-moz-box-shadow': '2px 2px 3px rgba(0, 0, 0, 0.3)',
            '-webkit-box-shadow': '2px 2px 3px rgba(0, 0, 0, 0.3)',
            'box-shadow': '2px 2px 3px rgba(0, 0, 0, 0.3)'
          });
        }

        if (scope.title != undefined && scope.title != '') {
          var panelTitle = element.find('.panel-title');
          panelTitle.css({
            //'cursor': 'pointer',
            'font-family': options.panelTitleFontFamily,
            'margin': '5px',
            'padding': '8px',
            '-moz-border-radius': options.borderRadius,
            '-webkit-border-radius': options.borderRadius,
            'border-radius': options.borderRadius,
            'border': options.panelTitleBorderStyle,
            'font-size': options.panelTitleFontSize,
            'font-weight': options.panelTitleFontWeight,
            'color': options.panelTitleColor,
            'filter': 'progid:DXImageTransform.Microsoft.gradient(startColorstr="' + options.panelTitleShadeStart + '", endColorstr="' + options.panelTitleShadeEnd + '")',
            'text-shadow': '1px 1px 2px rgba(0, 0, 0, 0.1)'
          });
          if (scope.minititle != undefined && scope.minititle == 'true') {
            panelTitle.css({
              'font-size': options.panelTitleFontSize / 3,
              'padding': '2px'
            });
          }
          panelTitle.css('background', '-webkit-gradient(linear, left top, left bottom, from(' + options.panelTitleShadeStart + '), to(' + options.panelTitleShadeEnd + '))');
          panelTitle.css('background', '-moz-linear-gradient(top, ' + options.panelTitleShadeStart + ', ' + options.panelTitleShadeEnd + ')');
          panelTitle.css('background', options.panelTitleShadeEnd);
        }

        var panelContent = element.find('.panel-content');
        panelContent.css({
          'margin': '5px',
          'padding': '8px',
          'color': 'black'
        });

      }
    };
  });
