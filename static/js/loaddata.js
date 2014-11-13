
jQuery.fn.loaddata = function( user_setting) {
    return this.each(function() {
        
        var opts = jQuery.extend({
            /* config */
            url : "",//显示指定url，如果未指定则从 url_attr中获取
            threshold : 100,//滚动加载阈值
            box : ".datalist",//容器
            load_mode : "scroll_append",//scroll_append  click_flush  click_append
            /* config */
        }, user_setting || {});
        
        var sys_opts = {
            page_loading : "data-loadding",//整页加载时容器ID
            url_attr : "get_data_url",//容器 加载数据 来源
            data_mode_attr :"data_mode",//设置容器加载数据后 的处理方式的attr
            loading_img : '<img src="/static/images/icon_feed_loading.gif" />'
        };
        
        var DATA_MODE_APPEND = "append";
        var DATA_MODE_FLUSH = "flush";
        
        function __init() {
            if (!$.loaddata_loadding){
                $.loaddata_loadding = false;
            }
            if( opts.box == "" ){
               return;
            }
            if (opts.url){
                $currentObj.attr(sys_opts.url_attr, opts.url);
            }
            if(!$currentObj.attr(sys_opts.url_attr)){
                return;
            }
            
            if(opts.load_mode == 'scroll_append'){
                bind_scroll_append();
            }else if(opts.load_mode == 'click_flush'){
                bind_click(DATA_MODE_FLUSH)
            }else if(opts.load_mode == 'click_append'){
                bind_click(DATA_MODE_APPEND)
            }
            
        }
        function bind_scroll_append(){
            $(window).scroll(function(){
                var srollPos = $(window).scrollTop()+$(window).height();    //滚动条距顶部距离(页面超出窗口的高度)
                var flowLine = $(opts.box).offset().top+$(opts.box).outerHeight()-opts.threshold;
                if(!$.loaddata_loadding){
                    if (flowLine < srollPos) {
                        $(opts.box).attr(sys_opts.data_mode_attr, DATA_MODE_APPEND);
                        load_data();
                    } 
                }
            });
        }
        function bind_click(data_mode){
            $currentObj.click(function(){
                $(opts.box).attr(sys_opts.data_mode_attr, data_mode);
                $(opts.box).attr(sys_opts.url_attr, $currentObj.attr(sys_opts.url_attr));
                if(!$.loaddata_loadding){
                    load_data();
                }
            });
        }
        
        function bind_click_flush(){
            $currentObj.click(function(){
                $(opts.box).attr(sys_opts.data_mode_attr, DATA_MODE_FLUSH);
                $(opts.box).attr(sys_opts.url_attr, $currentObj.attr(sys_opts.url_attr));
                if(!$.loaddata_loadding){
                    load_data();
                }
            });
        }
        function load_data(){
           $.loaddata_loadding = true;
           show_loading();
           var request_url=$(opts.box).attr(sys_opts.url_attr);
           if (request_url){
               $.get_data(
                    request_url, 
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
           var data_mode=$(opts.box).attr(sys_opts.data_mode_attr);
           if(data_mode == DATA_MODE_APPEND){
              $loaddingItem = $(opts.box).children(":first").clone();
              $loaddingItem.html(sys_opts.loading_img);
              $loaddingItem.appendTo($(opts.box));
              $loaddingItem.css("text-align","center");
           }else if(data_mode == DATA_MODE_FLUSH){
              var loaddingTag = "#"+sys_opts.page_loading;
              $loaddingItem = $(loaddingTag);
              var boxcss = 'background-color:#000;-moz-opacity:0.8; opacity:0.8;-khtml-opacity: 0.8;position:absolute;top:0px;left:0px;z-index:9999;display:hidden;';
              if($loaddingItem.length == 0){
                  $loaddingItem = $('<div id="'+data-loadding+'" style="display:none">'+sys_opts.loading_img+'</div>');
                  $("body").prepend($loaddingItem);
              }
              if(!$loaddingItem.attr("css_loaded")){
                  $loaddingItem.attr("style",boxcss);
              }
              var ww = $(window).width();
              var wh = $(window).height();
              var dw = $(document).width();
              var dh = $(document).height();
              $loaddingItem.width(dw);
              $loaddingItem.height(dh);
              $(loaddingTag+' img').css('position','fixed')
              $(loaddingTag+' img').css('top', (wh / 2 - 24));
              $(loaddingTag+' img').css('left', (ww / 2 - 24));
              $loaddingItem.show();
           }
        }
        function close_loading() {
           var data_mode=$(opts.box).attr(sys_opts.data_mode_attr);
           if(data_mode == DATA_MODE_APPEND){
              $loaddingItem.remove();
           }else if(data_mode == DATA_MODE_FLUSH){
              $loaddingItem.hide();
           }
           $.loaddata_loadding = false;
        }
        function process_data(data) {
           var data_mode=$(opts.box).attr(sys_opts.data_mode_attr);
           if(data_mode == DATA_MODE_APPEND){
              append_data(data)
           }else if(data_mode == DATA_MODE_FLUSH){
              flush_data(data)
           }
           if(data.url){
               $(opts.box).attr(sys_opts.url_attr, data.url);
           }else{
               $(opts.box).attr(sys_opts.url_attr, "");
           }
        }
        function append_data(data) {
           $(opts.box).append(data.html);
        }
        function flush_data(data) {
           $(opts.box).html(data.html);
        }
        var $currentObj = $(this);
        __init();
    });
}


