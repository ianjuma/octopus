angular.module('metricSlice')
  .factory('USSD', function($http) {
    return {
      save: function(User) {
        return $http.post('/api/user', { username: User.username, metric: User.metric,
          startDate: User.startDate, endDate: User.endDate, granularity: User.granularity });
      }
    };
  });
