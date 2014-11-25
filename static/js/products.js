$(function(){
  $(".filter_list li").click(function(){
     $(this).addClass('on');
     $(this).siblings().removeClass('on');
	 $(".product_category_list").hide();
	 $("."+$(this).find("div").attr('class')+"_list").show();
	 if($(this).find(".p_t_3").length>0){
	   show_filter_brand_box();
	 }else{
	   $(".brand_filter_box").hide();
	   $(".brand_filter_btn").removeClass("brand_filter_btn_up");
	 }
  });
  $(".product_category_list li").click(function(){
     var url=$(this).find("a").attr("href");
	 if(url){
       window.location = url;
	 }
	 return false;
  });
  $(window).scroll(function () {
      $(".brand_filter_box").hide();
	  $(".brand_filter_btn").removeClass("brand_filter_btn_up");
	  var srollPos = $(window).scrollTop();    //滚动条距顶部距离(页面超出窗口的高度)
	  var flowLine = $('.filter_list_box').offset().top-44;
	  if (flowLine < srollPos) {
	      $(".filter_flow_box").css('position', 'fixed');
	      $(".filter_flow_box").css('left',0);
		  $(".filter_flow_box").css('top',"44px");
	  } else {
	      $(".filter_flow_box").css('position', 'static');
	  }
  });
  function show_filter_brand_box(){
    $brand_filter_btn = $(".brand_filter_btn");
    if($(".brand_filter_box").is(":hidden")){
	   $(".brand_filter_box").css("top",($(".p_t_3").parent().offset().top+$(".p_t_3").parent().height()));
	   $(".brand_filter_box").show();
	   $brand_filter_btn.addClass("brand_filter_btn_up");
	}else{
	   $(".brand_filter_box").hide();
	   $brand_filter_btn.removeClass("brand_filter_btn_up");
	}
  }
});
