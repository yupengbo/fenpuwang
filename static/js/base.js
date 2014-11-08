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
																		      $(".feed_filter_box").hide();
																			       if(flowLine<srollPos&&$(".top_search").is(":hidden")){
																				            $('.icon_btn .search_icon').show();
																							     }else{
																								        $('.icon_btn .search_icon').hide();
																										     }
																											    }
																												 });
																												  /* feed筛选按钮 */
																												   $('.icon_btn .feed_filter').click(function(){
																												       if($(".feed_filter_box").is(":hidden")){
																													         var top=$('.nav').outerHeight()+$('.nav').offset().top;
																															       $(".feed_filter_box").css('top',top);
																																         $(".feed_filter_box").show();
																																		     }else{
																																			       $(".feed_filter_box").hide();
																																				       }
																																					    });
																																						});
																																						$.extend({
																																						    get_data : function(url, args, option_callback,datatype) {
																																							        datatype = datatype === null ? 'text': datatype.toUpperCase();
																																									        option_callback = option_callback === null ? $.success_callback : option_callback;
																																											        $.ajax( {
																																													            type : 'POST',
																																																            dataType : datatype.toLowerCase(),
																																																			            url : url,
																																																						            data : args,
																																																									            timeout : 1000,
																																																												            async : true,
																																																															            cache : true,
																																																																		            beforeSend : $.before_send_callback,
																																																																					            complete : $.complete_callback, // 接受数据完毕调用函数
																																																																								            success : option_callback,
																																																																											            error : $.error_callback
																																																																														        });
																																																																																    },
																																																																																	    success_callback : function(xmlReq) {
																																																																																		        
																																																																																				    },
																																																																																					    before_send_callback : function(xmlReq) {
																																																																																						        /**
																																																																																								        * 数据请求之前时执行
																																																																																										        */
																																																																																												        $.ajax_complete();
																																																																																														    },
																																																																																															    complete_callback : function(xmlReq, textStatus) {
																																																																																																        /**
																																																																																																		         * 数据获取完成时执行
																																																																																																				          */
																																																																																																						          $.ajax_complete();
																																																																																																								      },
																																																																																																									      /**
																																																																																																										       * 请求出现错误 responseText 请求的数据 data || textStatus 文本状态 eg：success
																																																																																																											        */
																																																																																																													    error_callback : function(xmlReq, textStatus) {
																																																																																																														        switch (xmlReq.status) {
																																																																																																																            case 404: // Not Found
																																																																																																																			                alert("XmlHttpRequest status: [404] \nThe requested URL was not found on this server.");
																																																																																																																							                break;
																																																																																																																											            case 500:
																																																																																																																														                alert("XmlHttpRequest status: [500] Service Unavailable");
																																																																																																																																		                break;
																																																																																																																																						            case 400:
																																																																																																																																									                alert("XmlHttpRequest status: [400] Bad Request");
																																																																																																																																													                break;
																																																																																																																																																	            case 503: // Service Unavailable
																																																																																																																																																				                alert("XmlHttpRequest status: [503] Service Unavailable");
																																																																																																																																																								                break;
																																																																																																																																																												            default:
																																																																																																																																																															                break;
																																																																																																																																																																			        }
																																																																																																																																																																					        $.ajax_complete();
																																																																																																																																																																							    },
																																																																																																																																																																								    ajax_complete : function(){
																																																																																																																																																																									        /*去掉菊花转*/
																																																																																																																																																																											        $("").html("");
																																																																																																																																																																													    }
																																																																																																																																																																														});  
