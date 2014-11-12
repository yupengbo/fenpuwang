$(function () {
    $('.download .close').click(function () {
        $('.download').hide();
    });
    var isIndexPage = $(".search_box").length > 0;
    if (isIndexPage) {
        $('.icon_btn .search_icon').hide();
    }
    $('.icon_btn .search_icon').click(function () {
        $(this).hide();
        $('.top_search').show();
        $('.nav ul').hide();
    });
    $('.top_search .close').click(function () {
        $('.top_search').hide();
        $('.nav ul').show();
    });

    $(window).scroll(function () {
        var srollPos = $(window).scrollTop();    //滚动条距顶部距离(页面超出窗口的高度)
        var flowLine = $('.nav_bar').offset().top;
        if (flowLine < srollPos) {
            $(".nav").css('position', 'fixed');
        } else {
            $(".nav").css('position', 'relative');
        }
        if (isIndexPage) {
            flowLine = $('.search_box').outerHeight() + $('.search_box').offset().top;
            $(".feed_filter_box").hide();
            if (flowLine < srollPos && $(".top_search").is(":hidden")) {
                $('.icon_btn .search_icon').show();
            } else {
                $('.icon_btn .search_icon').hide();
            }
        }
    });
    /* feed筛选按钮 */
    $('.icon_btn .feed_filter').click(function () {
        if ($(".feed_filter_box").is(":hidden")) {
            var top = $('.nav').outerHeight() + $('.nav').offset().top;
            $(".feed_filter_box").css('top', top);
            $(".feed_filter_box").show();
        } else {
            $(".feed_filter_box").hide();
        }
    });
});
$.extend({
    get_data: function (url, args, success_cb, completion_cb, datatype) {
        datatype = (datatype == null ? 'text' : datatype.toUpperCase());
        success_cb = (success_cb === null ? $.success_callback : success_cb);
        completion_cb = (completion_cb === null ? $.complete_callback : completion_cb);
        $.ajax({
            type: 'GET',
            dataType: datatype.toLowerCase(),
            url: url,
            data: args,
            timeout: 1000,
            async: true,
            cache: true,
            beforeSend: $.before_send_callback,
            complete: completion_cb,
            success: success_cb,
            error: $.error_callback
        });
    },
    show_loadding: function (xmlReq) {
        var ww = $(window).width();
        var wh = $(window).height();
        var dw = $(document).width();
        var dh = $(document).height();
        $('#data-loadding').width(dw);
        $('#data-loadding').height(dh);
        $('#data-loadding img').css('top', (wh / 2 - 24));
        $('#data-loadding img').css('left', (ww / 2 - 24));
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
        $.ajax_complete();
    },
    ajax_complete: function () {
        /*去掉菊花转*/
        $('#data-loadding').hide();
    }
});
