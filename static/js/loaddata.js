
jQuery.fn.loaddata = function( opts) {
    opts = jQuery.extend({
        url : "",
        threshold : 100,
        box : ".datalist",
        load_mode : "scroll",//scroll  click
        data_mode : "append",//append  flush
        loading_mode : "appendBox",//appendBox  page
        page_loading : "#data-loadding",
        loading_img : '<img src="/static/images/icon_feed_loading.gif" />'
    }, opts || {});
    return this.each(function() {
        function __init() {
           
            if (!$.loaddata_loadding){
                $.loaddata_loadding = false;
            }
            if( opts.url =="" || opts.box == "" ){
               return;
            }
            if(opts.load_mode == 'scroll'){
               bind_scroll();
            }else if(opts.load_mode == 'click'){
               bind_click();
            }
        }
        function bind_scroll(){
            $(window).scroll(function () {
                var srollPos = $(window).scrollTop()+$(window).height();    //滚动条距顶部距离(页面超出窗口的高度)
                var flowLine = $(opts.box).offset().top+$(opts.box).outerHeight()-opts.threshold;
                if(!$.loaddata_loadding){
                    if (flowLine < srollPos) {
                        load_data();
                    } 
                }
            });
        }
        function bind_click(){
            $currentObj.click(function(){
                load_data();
            });
        }
        function load_data(){
           $.loaddata_loadding = true;
           console.log("load---:"+$.loaddata_loadding);
           show_loading();
           if (opts.url){
               $.get_data(
                    opts.url, 
                    "",
                    function(data) {
                        process_data(data);
                    },
                    function(xmlReq, textStatus) {
                        close_loading();
                    }, 
                    'json'
                );
           }
        }
        var $loaddingItem ;
        function show_loading() {
           if(opts.loading_mode == 'appendBox'){
              $loaddingItem = $(opts.box).children(":first").clone();
              $loaddingItem.html(opts.loading_img);
              $loaddingItem.appendTo($(opts.box));
              $loaddingItem.css("text-align","center");
           }else if(opts.loading_mode == 'page'){
              if($(opts.page_loading).length == 0){
                  var boxcss = 'background-color:#000;-moz-opacity:0.8; opacity:0.8;-khtml-opacity: 0.8;position:absolute;top:0px;left:0px;z-index:9999;display:hidden;';
                  $loaddingItem = $('<div id="data-loadding" style="'+boxcss+'">'+opts.loading_img+'</div>');
                  $("body").prepend($loaddingItem);
              }
              var ww = $(window).width();
              var wh = $(window).height();
              var dw = $(document).width();
              var dh = $(document).height();
              $loaddingItem.width(dw);
              $loaddingItem.height(dh);
              $('#data-loadding img').css('position','fixed')
              $('#data-loadding img').css('top', (wh / 2 - 24));
              $('#data-loadding img').css('left', (ww / 2 - 24));
              $loaddingItem.show();
           }
        }
        function close_loading() {
           if(opts.loading_mode == 'appendBox'){
              $loaddingItem.remove();
           }else if(opts.loading_mode == 'page'){
              if($(opts.page_loading).length > 0){
                  $loaddingItem.hide();
              }
           }
           $.loaddata_loadding = false;
        }
        function process_data(data) {
           if(opts.data_mode == 'append'){
              append_data(data)
           }else if(opts.data_mode == 'flush'){
              flush_data(data)
           }
           if(data.url){
               opts.url=data.url;
           }else{
               opts.url="";
           }
        }
        function append_data(data) {
           $(opts.box).append(data.html);
        }
        function flush_data(data) {
           $(opts.box).html(data.html);
        }
        $currentObj = $(this);
        __init();
    });
}


