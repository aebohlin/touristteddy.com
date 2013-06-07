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

        $scope.comment = angular.copy(blankComment);

    };

    var blankComment = {
        comment: "",
        teddyId: 0,
        postId: 0,
        csrfmiddlewaretoken: ""
    };

    $scope.initComment = function (post) {
        $scope.comment.post_id = post.id;
        $scope.comment.teddy_id = post.teddy_id;
    }

    $scope.postComment = function () {
        $scope.csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        alert($scope.csrfmiddlewaretoken);
        //'X-CSRFTOKEN'
        var url = "/teddys/" + $scope.comment.teddy_id + "/posts/" + $scope.comment.post_id + "/comments/add";
        $http.post(url, $scope.comment, {headers: {'X-CSRFTOKEN': $scope.csrfmiddlewaretoken}}).success(function (data) {
            alert(data);
        });

        //  $http.post("/teddys/" + post.teddy.id + "/posts/" post.id + "/comments/add",
        // {
        //     comment: comment.comment,
        //     csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        // }).success(funcation (data) {
        //     alert(data);
        // });

    };


}
