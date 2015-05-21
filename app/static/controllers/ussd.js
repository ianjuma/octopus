angular.module('metricSlice')
  .controller('UssdController', function($scope, $alert, USSD) {
    //.$promise
    $scope.addUSSD = function() {
      USSD.save({ username: $scope.username, metric: $scope.metric,
        granularity: $scope.granularity, startDate: $scope.startDate, endDate: $scope.endDate })
        .then(function(result) {
          console.log(result);
          $scope.username = result.username;
          $scope.metric = result.metric;
          $scope.granularity = result.granularity;
          $scope.startDate = result.startDate;
          $scope.endDate = result.endDate;
          $scope.addForm.$setPristine();
          $alert({
            content: 'Request is being processed.',
            animation: 'fadeZoomFadeDown',
            type: 'material',
            duration: 4
          });
        })
        .catch(function(response) {
          $scope.username = '';
          $scope.metric = '';
          $scope.granularity = '';
          $scope.startDate = '';
          $scope.endDate = '';
          $scope.addForm.$setPristine();
          $alert({
            content: response.data.message,
            animation: 'fadeZoomFadeDown',
            type: 'material',
            duration: 4
          });
        });
    };
  });
