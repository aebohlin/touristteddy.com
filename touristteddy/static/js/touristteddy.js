$(document).ready(function () {
	$(".fppost a.open-fancy").fancybox();

	$(".fancy").each(function () {
		touristteddy.DAL.loadComments($(this));
  	});

	$('.commentText').bind("enterKey",function(e){
   		var $commentText = $(this);
  		$.ajax({
			url: $commentText.data("url"), 
			method: 'POST',
			data: { comment: $commentText.val(), csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value },
			success:function (result) {
				if(result == true) {
					touristteddy.DAL.loadComments($commentText.parents(".fancy"));
					$commentText.val('');
				}
			}
		});	
	});
	$('.commentText').keyup(function(e){
		if(e.keyCode == 13) {
			$(this).trigger("enterKey");
		}
	});

	$("#showCreateForm").click(function (e) {
		e.preventDefault();
		$(".form-1.create").show();
	});
});

touristteddy = {}
touristteddy.DAL = {
	loadComments: function ($fancy) {
		var $comments = $fancy.find(".comments");
		$comments.html('');
		$.ajax({
			url: $comments.data("url"), 
			success:function (result) {
				for (var i = 0; i < result.length; i++) {
					var comment = result[i][0];
					var username = result[i][1];
					var userid = result[i][2];
					var datetime = result[i][3];
					$comments.append('<div class="comment"><a href="/users/' + userid + '/" class="user">' + username + '</a> <span class="text">' + comment + '</span><span class="datetime">' + datetime + '</span></div>');					
				};
			}
		});	
	}

}

