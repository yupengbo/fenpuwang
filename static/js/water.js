var isiOS = navigator.userAgent.match('iPad')|| navigator.userAgent.match('iPhone')|| navigator.userAgent.match('iPod'), isAndroid = navigator.userAgent.match('Android'),isDesktop = !isiOS&&!isAndroid;
var _hmt = _hmt || [];
function activity_shared(fee){
  if (share_fee==0){
    share_fee = fee;
  }
  $("#share_bonus").hide();
  $("#opened").hide();
  $("#view_result").show();
  change_tip(fee);
}
function to_share(){
   $('.weixin_share').show();
}
function hide_share_mask(){
   $('.weixin_share').hide();
}
function addCookie(objName,objValue,objHours){//添加cookie
    var str = objName + "=" + escape(objValue);
    if(objHours > 0){//为0时不设定过期时间，浏览器关闭时cookie自动消失
        var date = new Date();
        var ms = objHours*3600*1000;
        date.setTime(date.getTime() + ms);
        str += "; expires=" + date.toGMTString() + ";path=/";
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
