$(function(){
 if( $(".product_cell_link").length > 0){
   var $product_link = $(".product_cell_link").eq(0);
   var link_html = $product_link.html();
   link_html = "<div class='con fcb1'><div class='link_cell product_cell_link'>" + link_html + "</div></div>" 
   $(".content").html($(".content").html()+link_html);
   $(".product_cell_link:last").show();
 }
});
