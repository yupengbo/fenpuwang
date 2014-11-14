$(function(){
  $(".filter_list li").click(function(){
     $(this).addClass('on');
     $(this).siblings().removeClass('on');
	 $(".product_category_list").hide();
	 $("."+$(this).find("div").attr('class')+"_list").show();
  });
  $(".product_category_list li").click(function(){
     var url=$(this).find("a").attr("href");
	 if(url){
       window.location = $(this).find("a").attr("href");
	 }
	 return false;
  });
});
