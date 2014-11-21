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
  $(".product_list li").click(function(){
    var url=$(this).find("div a").attr("href");
    if(url){
       window.location = url;
    }
    return false;
  });
});
