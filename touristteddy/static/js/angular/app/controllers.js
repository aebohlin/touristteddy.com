'use strict';

//function PostCtrl($scope, $http) {
//    $scope.init = function (url) {
//        $http.get(url).success(function (data) {
//            $scope.comments = data;
//        });
//    };
//}

function PostsCtrl($scope, $http) {
    $scope.init = function (url) {
        $http.get(url).success(function (data) {
            $scope.posts = data;
        });
    };
    $scope.postComment = function (post) {
        alert(post.title);
    };
}