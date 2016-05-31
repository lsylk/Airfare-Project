

"use strict";
        var app = angular.module('flightApp',['ngMaterial', 'ngMessages', 'material.svgAssetsCache', 'ngAnimate', 'ui.bootstrap' ]);
        app.controller('ctrlForm', ["$scope", function($scope) {
            $scope.departure = "LAX";
            $scope.arrival = "SFO";
            $scope.departure_date = new Date(); // "2016-10-11 ==> 11/11/2016"
            $scope.mindate = new Date();
            $scope.return_date = null;
            $scope.results = 1;

            $scope.choiceDeparture = "SFO";
            $scope.choiceArrival = "LAX";
            $scope.choiceDepartureDate = new Date();
            $scope.choiceResult = 1;

            $scope.showcalendar = function ($event) {
                $scope.showdp = true;
            };

            $scope.showdp = false;
  
            $scope.choices = [{id: 'choice1'}, {id: 'choice2'}];

            $scope.choices.result = 1;
  
            $scope.addNewChoice = function() {
            var newItemNo = $scope.choices.length+1;
            $scope.choices.push({'id':'choice'+newItemNo});
            };
        
            $scope.removeChoice = function() {
            var lastItem = $scope.choices.length-1;
            $scope.choices.splice(lastItem);
            };

        }])
                .directive('formOneway', function() {
          return {
            templateUrl: '/static/html/one_way_form.html'
          };
        })
             .directive('formRoundtrip', function() {
          return {
            templateUrl: '/static/html/round_trip_form.html'
          };
        })
             .directive('formMulticity', function() {
          return {
            templateUrl: '/static/html/multi_city_form.html'
          };
        });