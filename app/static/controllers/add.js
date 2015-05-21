angular.module('metricSlice')
  .controller('AddController', function($scope, $alert, User) {
    //.$promise
    $scope.addUser = function() {
      User.save({ name: $scope.name, age: $scope.age, id: $scope.id })
        .then(function(result) {
          console.log(result);
          $scope.name = result.name;
          $scope.age = result.age;
          $scope.id = result.id;
          $scope.addForm.$setPristine();
          $alert({
            content: 'Request is being processed.',
            animation: 'fadeZoomFadeDown',
            type: 'material',
            duration: 4
          });
        })
        .catch(function(response) {
          $scope.name = '';
          $scope.age = '';
          $scope.id = '';
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
