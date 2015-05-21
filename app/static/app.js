angular.module('metricSlice', ['ngResource', 'ngMessages', 'ngRoute', 'ngAnimate', 'mgcrea.ngStrap'])
  .config(function ($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true);

    $routeProvider
      .when('/', {
        templateUrl: 'static/views/add.html',
        controller: 'AddController'
      })
      .when('/ussd', {
        templateUrl: 'static/views/ussd.html',
        controller: 'UssdController'
      })
      .when('/detail', {
        templateUrl: 'static/views/detail.html',
        controller: 'DetailController'
      })
      .when('/main', {
        templateUrl: 'static/views/main.html',
        controller: 'MainController'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
