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
        if(url != '') {
            $http.get(url).success(function (data) {
                $scope.posts = data;
            });
        }
        $scope.comment = angular.copy(blankComment);
        $scope.post = angular.copy(blankPost);
        $scope.editing = false;
    };

    var blankComment = {
        comment: "",
        teddyId: 0,
        postId: 0,
        csrfmiddlewaretoken: ""
    };


    var blankPost = {
        title: "",
        description: "",
        latitude: "",
        longitude: "",
        teddy_id: "",
        csrfmiddlewaretoken: ""
    };

    $scope.loadMap = function () {
        if($scope.editing) {
            google.maps.event.trigger(map, "resize");
            google.maps.event.addListener(map, 'click', function(event) {
                placeMarker(event.latLng);
            });
        }
        return $scope.editing;
    };

    $scope.addPost = function () {
        $scope.latitude = lat;
        $scope.longitude = lng;
        alert('tst');
        $scope.csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        var url = "/teddys/" + $scope.post.teddy_id + "/posts/add";
        $http.post(url, $scope.post, {headers: {'X-CSRFTOKEN': $scope.csrfmiddlewaretoken}}).success(function (data) {
            alert(data.title)
            //post.comments.push(data);
            // $scope.comment.comment = '';
            // var $comments = $('#' + post.id + ' .comments');
            // window.setTimeout(function() {
            //     $comments.scrollTop($comments.prop("scrollHeight"));
            // }, 1000);

        });
        return false;
    }

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
