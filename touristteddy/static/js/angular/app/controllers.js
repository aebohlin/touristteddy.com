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
        $scope.editing = false;
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
    };

    $scope.postComment = function (post) {
        $scope.csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        var url = "/teddys/" + post.teddy_id + "/posts/" + post.id + "/comments/add";
        $http.post(url, $scope.comment, {headers: {'X-CSRFTOKEN': $scope.csrfmiddlewaretoken}}).success(function (data) {
            post.comments.push(data);
            $scope.comment.comment = '';
            var $comments = $('#' + post.id + ' .comments');
            window.setTimeout(function() {
                $comments.scrollTop($comments.prop("scrollHeight"));
            }, 1000);

        });

    };


}
