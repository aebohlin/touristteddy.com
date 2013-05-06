'use strict';

function PostCtrl($scope, $http) {
    $scope.init = function (url) {
        $http.get(url).success(function (data) {
            $scope.comments = data;
        });
    };
}