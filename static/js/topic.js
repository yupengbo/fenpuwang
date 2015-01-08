$(function(){
 if( $(".product_cell_link").length > 0){
   $(".footer_download").hide();
   var $product_link = $(".product_cell_link").eq(0);
   var link_html = $product_link.html();
   link_html = "<div class='footer_product'><div class='footer_product_inner'>" + link_html + "</div></div>" 
   $(".footer").html(link_html);
   $(".footer .topic_product_text").html("<div class='footer_product_tip'>本文提到的商品</div>" + 
      $(".footer .topic_product_text").html() +
	  "<div class='fl footer_product_seller_info'><span class='seller_name'>卖家：美丽出品</span><span class='fenpu_info'>粉扑担保：直邮认证 无理由退货</span></div>" 
   );
   $(".footer .topic_product_text .topic_product_price").addClass("fl");
   $(".footer .link_arrow .link_arrow_i").removeClass("link_arrow_i");
 }
});
