$(function(){
 $('.download .close').click(function(){
     $('.download').hide();
	  });
	   var isIndexPage=$(".search_box").length>0;
	    if(isIndexPage){
		   $('.icon_btn .search_icon').hide();
		    }
			 $('.icon_btn .search_icon').click(function(){
			     $(this).hide();
				     $('.top_search').show();
					     $('.nav ul').hide();
						  });
						   $('.top_search .close').click(function(){
						       $('.top_search').hide();
							       $('.nav ul').show();
								    });
									 
									  $(window).scroll(function(){
									     var srollPos = $(window).scrollTop();    //滚动条距顶部距离(页面超出窗口的高度)  
										    var flowLine=$('.nav_bar').offset().top;
											   if(flowLine < srollPos ) {  
											         $(".nav").css('position','fixed');
													    }else{
														      $(".nav").css('position','relative');
															     }
																    if(isIndexPage){
																	     flowLine=$('.search_box').outerHeight()+$('.search_box').offset().top;
																		      if(flowLine<srollPos){
																			         $('.icon_btn .search_icon').show();
																					      }else{
																						         $('.icon_btn .search_icon').hide();
																								      }
																									     }
																										  }); 
																										  });

