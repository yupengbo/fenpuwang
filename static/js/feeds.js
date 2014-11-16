$(function(){
  $(".feed_filter_box li").click(function(){
    $(this).addClass('on');
    $(this).siblings().removeClass('on'); 
  });
  show_right_info();
});

function show_right_info(){
   var wh = $(window).width();
   $('.datalist .rhinfo').each(function(){
      var $rhinfo=$(this);
	  var rhinfow=$rhinfo.width();
      var targetBoxClass = $rhinfo.attr('target');
	  if(!targetBoxClass){
		 return;
	  }
	  $box = $rhinfo.parent();
      $targetBox = $box.find("." + targetBoxClass);
	  $positionEm = $box.find("." + targetBoxClass + " em");
	  if($targetBox.length == 0 || $positionEm.length == 0){
		 return;
	  }
      var eml = $positionEm.offset().left;
	  if (eml + rhinfow > wh-15){
	     $("<br/>").insertBefore($positionEm);
	  }
	  $positionEm = $box.find("." + targetBoxClass + " em");
	  var rhinfotop = $positionEm.offset().top - $box.offset().top;
	  $rhinfo.css("position","absolute");
	  $rhinfo.css("top",rhinfotop);
	  $rhinfo.css("right",0);
	  $rhinfo.show();
   });
}
