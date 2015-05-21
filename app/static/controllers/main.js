angular.module('metricSlice')
    .controller('MainController', function($scope) {
        $scope.title = ['0-9', 'A', 'B', 'C', 'D'];
        $scope.things = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy',
            'Crime', 'Documentary'];
        $scope.docTitle = "Not Much here"
    });
