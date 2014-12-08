var isiOS = navigator.userAgent.match('iPad')|| navigator.userAgent.match('iPhone')|| navigator.userAgent.match('iPod'), isAndroid = navigator.userAgent.match('Android'),isDesktop = !isiOS&&!isAndroid;
var _hmt = _hmt || [];
$(function () {
    $('.download .close').click(function () {
        $('.download').hide();
        show_right_info();
		addCookie('closedownload',1,7*24);
    });
    var isIndexPage = $(".search_box").length > 0;
    if (isIndexPage) {
        $('.icon_btn .search_icon').hide();
    }
    
	$('.top_search .close').click(function () {
        $('.nav ul').show();
		$("#nav_keyword").hide();
		$('.top_search .closebox').hide();
        $("#nav_btn_search").removeClass("on");
		show_nav_search();
    });
    $("#nav_btn_search").click(function(){
	   if($(this).hasClass("on")){
	      search_all($("#nav_keyword").val());
	   }else{
	      $('.top_search .closebox').show();
		  $("#nav_keyword").show();
		  $('.nav ul').hide();
		  $("#nav_keyword").focus();
		  $(this).addClass("on");
	   }
	});
	$("#index_btn_search").click(function(){
       search_all($("#index_keyword").val());
    });
    function show_nav_search(){
	   var srollPos = $(window).scrollTop();
	   if (isIndexPage) {
            var flowLine = $('.search_box').outerHeight() + $('.search_box').offset().top;
            $(".feed_filter_box").hide();
            if (flowLine < srollPos ) {
                $('#nav_btn_search').show();
            } else {
                $('#nav_btn_search').hide();
            }
	   }
	}
	function search_all(keyword){
	    if(keyword && trimStr(keyword)!=""){
		    window.location = '/search/' + encodeURIComponent(keyword);
		}
		return false;
	}
	/*
    $(window).scroll(function () {
        var srollPos = $(window).scrollTop();    //滚动条距顶部距离(页面超出窗口的高度)
        var flowLine = $('.nav_bar').offset().top;
        if (flowLine < srollPos) {
            $(".nav").css('position', 'fixed');
			$(".nav").css('left',($(window).width()-$(".nav").width())/2);
        } else {
            $(".nav").css('position', 'relative');
			$(".nav").css('left',0);
        }
		show_nav_search();
    });
	*/
    /* feed筛选按钮 */
    $('.feed_filter').click(function () {
        if ($(".feed_filter_box").is(":hidden")) {
            var top = $('.nav').outerHeight() + $('.nav').offset().top;
            $(".feed_filter_box").css('top', top);
            $(".feed_filter_box").show();
        } else {
            $(".feed_filter_box").hide();
        }
    });
	$(window).resize(function (){
	   show_right_info();
	});
});
$.extend({
    get_data: function (url, args, success_cb, completion_cb, datatype) {
        datatype = (datatype == null ? 'text' : datatype.toUpperCase());
        success_cb = (success_cb === null ? $.success_callback : success_cb);
        completion_cb = (completion_cb === null ? $.complete_callback : completion_cb);
        $.ajax({
            type: 'POST',
            dataType: datatype.toLowerCase(),
            url: url,
            data: args,
            timeout: 10000,
            async: true,
            cache: true,
            beforeSend: $.before_send_callback,
            complete: completion_cb,
            success: success_cb,
            error: $.error_callback
        });
    },
    success_callback: function (xmlReq) {
        $.ajax_complete();
    },
    before_send_callback: function (xmlReq) {

    },
    complete_callback: function (xmlReq, textStatus) {
        /**
         * 数据获取完成时执行
         */

    },
    /**
     * 请求出现错误 responseText 请求的数据 data || textStatus 文本状态 eg：success
     */
    error_callback: function (xmlReq, textStatus) {
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
    }
});
function openapp(obj){
   var timeout, t=1000, hasApp = true;
   setTimeout(function(){
	 if(!hasApp){
	   window.location = 'http://www.dabanniu.com/download.phtml';
	 }
   },2000);
   var t1 = Date.now();
   var ifr = document.createElement("iframe"); 
   ifr.setAttribute('src', $(obj).attr("schemeUrl")); 
   document.body.appendChild(ifr); 
   timeout = setTimeout(function () {  
       var t2 = Date.now();
       if (!t1 || t2 - t1 < t + 100) {
	     hasApp = false;
       }
   },t);

}
function trimStr(str){
    return str.replace("/(^\s*)|(\s*$)/g","");
}
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
function addCookie(objName,objValue,objHours){//添加cookie
    var str = objName + "=" + escape(objValue);
    if(objHours > 0){//为0时不设定过期时间，浏览器关闭时cookie自动消失
        var date = new Date();
        var ms = objHours*3600*1000;
        date.setTime(date.getTime() + ms);
        str += "; expires=" + date.toGMTString();
     }
     document.cookie = str;
}

function getCookie(objName){//获取指定名称的cookie的值
     var arrStr = document.cookie.split("; ");
     for(var i = 0;i < arrStr.length;i ++){
        var temp = arrStr[i].split("=");
        if(temp[0] == objName) return unescape(temp[1]);
     } 
}

function delCookie(name){//为了删除指定名称的cookie，可以将其过期时间设定为一个过去的时间
     var date = new Date();
     date.setTime(date.getTime() - 10000);
     document.cookie = name + "=a; expires=" + date.toGMTString();
}

