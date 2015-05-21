angular.module('metricSlice')
  .factory('User', function($http) {
    return {
      save: function(User) {
        return $http.post('/api/user', { name: User.name, age: User.age, id: User.id });
      },
      getUser: function(_id) {
        return $http.get('/api/user', _id);
      }
    };
  });
