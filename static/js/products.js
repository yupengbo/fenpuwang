$(function(){
  $(".brand_filter_btn").css('left',($(".p_t_3").offset().left+30));
  $(".brand_filter_btn").show();
  $(".filter_list li").click(function(){
     $(this).addClass('on');
     $(this).siblings().removeClass('on');
	 $(".product_category_list").hide();
	 $("."+$(this).find("div").attr('class')+"_list").show();
	 if($(this).find(".p_t_3").length>0){
	   show_filter_brand_box();
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
  });
  function show_filter_brand_box(){
    $brand_filter_btn = $(".brand_filter_btn");
    if($(".brand_filter_box").is(":hidden")){
	   $(".brand_filter_box").show();
	   $brand_filter_btn.addClass("brand_filter_btn_up");
	}else{
	   $(".brand_filter_box").hide();
	   $brand_filter_btn.removeClass("brand_filter_btn_up");
	}
  }
});
