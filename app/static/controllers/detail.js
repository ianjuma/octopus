angular.module('metricSlice')
    .controller('DetailController', function($scope, $alert, User) {
        //.$promise
        User.getUser()
            .then(function(result) {
                $scope.User = result.data['Response'];
            })
            .catch(function(response) {
                $scope.name = '';
                $scope.age = '';
                $scope.id = '';
                $alert({
                    content: response.data.message,
                    animation: 'fadeZoomFadeDown',
                    type: 'material',
                    duration: 4
                });
            });
    });
