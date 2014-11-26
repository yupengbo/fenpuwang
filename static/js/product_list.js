$(function(){
  $(".filter_list li").click(function(){
	 var $libox = $(this).find("div");
	 if ($libox.hasClass("p_f_3")||$libox.hasClass("p_f_4")){  
	   if ($(this).hasClass("on")&&$libox.hasClass("p_f_4")){
	     $libox.attr("class","p_f_3");
		 $(this).attr("get_data_url",$(this).attr("get_data_url_1"));
	   }else{
	     $libox.attr("class","p_f_4");
	     $(this).attr("get_data_url",$(this).attr("get_data_url_2"));
	   }
	 }else{
       $(".filter_list li .p_f_4").attr("class","p_f_4"); 
	   $(".filter_list li .p_f_3").attr("class","p_f_4");
	   var $pricelibox = $(".filter_list li .p_f_4").parent();
	   $pricelibox.attr("get_data_url",$pricelibox.attr("get_data_url_1"));
	 }
	 $(this).addClass('on');
     $(this).siblings().removeClass('on');
  });
  $(window).scroll(function () {
	   var srollPos = $(window).scrollTop();    //滚动条距顶部距离(页面超出窗口的高度
	   var flowLine = $('.filter_list_box').offset().top-44;
	   if (flowLine < srollPos) {
	       $(".filter_flow_box").css('position', 'fixed');
	       $(".filter_flow_box").css('left',0);
	       $(".filter_flow_box").css('top',"44px");
	   } else {
           $(".filter_flow_box").css('position', 'static');
       }
  });
});
