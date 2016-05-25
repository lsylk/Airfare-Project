"use strict";

    <script src="http://ajax.googleapis.com/ajax/libs/angularjs/1.4.8/angular.min.js"></script>

        var app = angular.module('flightsApp', []);
        app.controller('controlForm', function($scope) {
            $scope.departure = "LAX";
            $scope.arrival = "SFO";
            $scope.departure_date = new Date(); // "2016-10-11 ==> 11/11/2016"
            $scope.results = 1;
        });


        angular.module('TabsApp', [])
        .controller('TabsCtrl', ['$scope', function ($scope) {
            $scope.tabs = [{
                    title: 'One',
                    url: 'one.tpl.html'
                }, {
                    title: 'Two',
                    url: 'two.tpl.html'
                }, {
                    title: 'Three',
                    url: 'three.tpl.html'
            }];

            $scope.currentTab = 'one.tpl.html';

            $scope.onClickTab = function (tab) {
                $scope.currentTab = tab.url;
            }
            
            $scope.isActiveTab = function(tabUrl) {
                return tabUrl == $scope.currentTab;
            }
        }]);