$(document).ready(function () {
	$(".fppost a.open-fancy").fancybox();

	$(".fancy").each(function () {
		var $comments = $(this).find(".comments");
		
		$.ajax({
			url:$comments.data("url"), 
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
  	});
});