$(function(){
  var yen_char='￥';
  function get_num(num,ret_val){
    num = Number(num);
    if(isNaN(num)){
	  return ret_val;
	}else{
	  return num;
	}
  }
  function get_goods_num(){
    var num = 0 ;
     $('.cart_list').eq(0).find("li").each(function(i,val) {
	    if($(this).find(".selector").hasClass("on")){
	        var	temp_num = get_num($(this).find('.num_input').val(),1);
	    	num = num + temp_num;
		}
	 });
	return num;
  }
  function get_total_fee(){
     var total_fee = 0;
     $('.cart_list').eq(0).find("li").each(function(i,val) {
	    if($(this).find(".selector").hasClass("on")){
	        var price = get_num($(this).find('.price_input').val(),0);
    		var num = get_num($(this).find(".num_input").val(),1);
	    	total_fee = total_fee + num * price;
		}
	 });
	 return total_fee;
  }
  $(".submitOrder").click(function(){
     if (get_total_fee()>0){
         $('#cart_form').submit();
	 }
  });
  function reset_val(){
    $('.total_fee em').html(yen_char + get_total_fee());
    $('.total_num em').html( get_goods_num());
    $('.total_info .fee em').html($('.total_fee em').html());
	$('#order_total_fee').val(get_total_fee());
  }
  $('.selector').click(function(){
	 if($(this).hasClass("on")){
	   $(this).removeClass("on");
	 }else{
	   $(this).addClass("on");
	 }
	 reset_val();
  });
  $('.del_btn').click(function(){
     $(this).parent().parent().remove();
	 reset_val();
  });
  $('.controll_box .minus').click(function(){
    var	num = get_num($(this).parent().find(".num_input").val(),1);
	num = num - 1;
	if (num<1){
       num = 1;
    }
	$(this).parent().find(".num_input").val(num);
	reset_val();
  });
  $('.controll_box .plus').click(function(){ 
    var num = get_num($(this).parent().find(".num_input").val(),1);
    num = num + 1;
	$(this).parent().find(".num_input").val(num);
	reset_val();
  });
  $(".num_input").change(function(){
    var	num = get_num($(this).val(),1);
	$(this).val(num);
    reset_val();
  });
  reset_val();
  $(".footer_download").hide();
})
