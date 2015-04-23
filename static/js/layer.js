$(document).ready(function(){
   bind_product_info();
   $(".cover_layer").click(function(){
      $(".exit_btn").click();
   });
   $(".exit_btn").click(function(){
     $(".product_more_standard").hide();
     $(".product_cart_container").show();
     $(".cover_layer").hide();
     $("#main-content").height('auto');
     $("#main-content").css('overflow','auto');
     current_num = 1;
     $(".product_num").html(1);
     var position_id = $(this).attr("id");
     document.getElementById(position_id).scrollIntoView();
   });
});


function bind_product_info(){
     ajax_product_info();
 }
function unbind_product_info(){
     $(".recommend_in_cart").unbind("click");
     $(".product_in_cart").unbind("click;")
     ajax_product_info();
 }
function ajax_product_info(){
   $(".recommend_in_cart").click(function(){
      var info_url =$(this).attr("product_info_url");
      var current_productId = $(this).attr("product_info_url").split("/")[3];
      $(".exit_btn").attr("id",current_productId);
      $.ajax({
        url:info_url,
        beforeSend:function(){
                     $(".product_layer_info").children().eq(0).nextAll().remove();
                     $(".haha").remove();
                     $(".top_split_line").nextUntil(".bottom_split_line").remove();
                  },
        success:function(data){
                  for(var i=0;i<(data.product.pics).length;i++){
                      if(i==0){
                         $(".product_info_img").attr("src",data.product.pics[i].org);
                      }
                  }
                  $(".product_layer_info").children().eq(0).html(data.product.name);
                  for(var i=0;i<(data.product.goods).length;i++){
                        $(".product_layer_info").append("<div style='margin-top:3px;display:none;' class='product_fixed_ps' goodsId="+data.product.goods[i]["goodsId"]+"><span style='color:#ff5346;font-size:14px;'>¥"+data.product.goods[i]["goodsPrice"]+"</span><span style='color:#dbdbdb;font-size:10px;'>/"+data.product.goods[i]["size"]+"</span></div>");
                        $(".product_more_standard").children().eq(0).after("<div style='height:36px;min-width:85px;margin-left:5%;margin-top:16px;' class='float_l haha'><div style='border:1px solid #666;font-size:12px;line-height:36px;padding-left:5px;padding-right:5px;' class='center abc' sizeId="+data.product.goods[i]["goodsId"]+">"+data.product.goods[i]["size"]+"</div></div>");
                        $(".top_split_line").after("<div style='display:none;height:85px;margin-left:5%;line-height:40px;font-size:12px;' class='product_send_time' timeId="+data.product.goods[i]["goodsId"]+">"+data.product.goods[i]["transportTitle"]+"</div>");
                  }
                  complete(current_productId);
                }
      });
   });
}

function complete(productId){
  $(".cover_layer").show();
  $("#main-content").height($(window).height()-200);
  //$("#main-content").css("margin-top",$(window).scrollTop()*(-1));
  //$("#main-content").height($(window).height()-200);
  //$("#main-content").css('overflow','hidden');
  $("#main-content").css('overflow','hidden');
  $(".haha").eq(0).children().css("border","2px solid #ff5346");
  $(".abc").eq(0).addClass("current")
  $(".product_fixed_ps").eq(0).show();
  $(".product_more_standard").show();
  $(".product_send_time").eq(0).show();
  $(".product_cart_container").hide();
  var product_layer_info_width = ($(".product_more_standard").width())*0.9 - 68 - 30;
  $(".product_layer_info").css("width",product_layer_info_width);
  $(".abc").click(function(){
     $(this).css("border","2px solid #ff5346");
     $(".abc").removeClass("current");
     $(this).addClass("current");
     $(".haha div").not($(this)).css("border","1px solid #dbdbdb");
     var size = $(this).attr("sizeId");
     $(".product_fixed_ps[goodsId="+size+"]").show();
     $(".product_fixed_ps[goodsId!="+size+"]").hide();
     $(".product_send_time[timeId="+size+"]").show();
     $(".product_send_time[timeId!="+size+"]").hide();
  });
  $(".product_in_cart").click(function(){
      var add_cart_url = $(".product_in_cart").attr("add_cart_url");
      var num = $(".product_num").html();
      var current_goodsId = $(".current").attr("sizeId");
      $.ajax({
        url:add_cart_url,
        data:"goodsId="+current_goodsId+"&productId="+productId+"&num="+num,
        success:function(data){
                   var new_cart_num = parseInt($(".product_cart_num").html())+parseInt(num);
                   $(".product_cart_num").html(new_cart_num);
                }
      });
      $(".exit_btn").click();
  });
}
