$(function(){
  $(".feed_filter_box li").click(function(){
    $(this).addClass('on');
    $(this).siblings().removeClass('on'); 
  });
  var isLoadingNextPage = false;  //是否正在加载更多答案
  $(window).scroll(function(){
      var mark = $("#mark").val();
	  var category_id = $("#category_id").val();
      if($(window).scrollTop() == ($(document).height() - $(window).height()) &&
          mark > 0 && isLoadingNextPage == false) {
          var url = "/feed/category/" + category_id + "/mark/" + mark + "/";
          isLoadingNextPage = true;
          $.get_data(url, null,function(data) {
              $("#mark").val(data.mark);
              $(".feedsList").append(data.html);
          },
          function(xmlReq, textStatus) {
              isLoadingNextPage = false;
          }, 'json');
      }
  });
  $('.datalist .title em').each(function(){ 
  });
});
