//begin   资源定义
var __res_b = "/static/images/";
var __get_cash_coupon_api = "/game/makeup/get";
function set_get_cash_coupon_api(api){
    __get_cash_coupon_api = api;
}
function get_get_cash_coupon_api(api){
    return __get_cash_coupon_api;
}
function res(res_url){
    return __res_b + res_url;
}
var welcome_scene_resources = [
   res('bg_home_02.jpg'),
   res('img_home_name_text.png'),
   res('img_home_left_lipstick.png'),
   res('img_home_right.png'),
   res('img_home_bottom.png'),
   res('btn_home_go.png'),
   res('img_qustion_top_right.png'),
   res('img_qustion_top_left.png'),
   res('bg_question_photo_zone.png'),
   res('btn_qustion_q_and_a_topic.png'),
   res('bg_qustion_q_and_a.png'),
   res('bg_questions.png'),
   res('icon_question_q_and_a_right.png'),
   res('icon_question_q_and_a_wrong.png')
];
var game_scene_resources=[

];
var finish_scene_resources=[
   res('img_final.png'),
   res('btn_checkout.png'),
   res('bg_questions.png')
];
var result_scene_resources=[
   res('bg_question_photo_zone.png'),
   res('btn_result.png'),
   res('img_result_fenpu.png'),
   res('bg_popover_01.png'),
   res('img_popover_download.png')
];
for (i=1;i<=15;i++) {
    var num = i;
    if( i<10){
        num = "0"+i;
    }
    game_scene_resources.push(res('icon_question_num_'+num+'.png'));
    game_scene_resources.push(res('img_progressbar_'+num+'.png'));
}
//end     资源定义

//答题操作次数
var __op_num = 0;
//问题总数
var __question_num = 1;
//当前正在回答的问题的序号
var __curr_question = 1;
//游戏开始时间
var __begin_time = 0;
//游戏结束时间
var __end_time = 0;
//题库
var __question_list;
//分数
var __user_score = 0;

var __question_ready = false;
var __welcome_res_ready = false;
var __can_answer = false;
function welcome_res_loaded(){
    $("#welcome_box").css("background-image","url('"+res('bg_home_02.jpg')+"')");
    $("#welcome_box .lipstick").attr("src",res('img_home_left_lipstick.png'));
    $("#welcome_box .title").attr("src",res('img_home_name_text.png'));
    $("#welcome_box .cloud").attr("src",res('img_home_right.png'));
    $("#welcome_box .bottom").attr("src",res('img_home_bottom.png'));
    $("#welcome_box .go").attr("src",res('btn_home_go.png'));
    __welcome_res_ready = true;
    to_welcome();
}
function question_loaded(data){
    __question_list = data;
    __question_num = data.length;
    __question_ready = true;
    to_welcome();
}
function to_welcome(){
    if(__question_ready&&__welcome_res_ready){
        $("#loading_box").hide();
        $("#welcome_box").show();
    }
}
function game_res_loaded(){
    $("#game_box").css("background-image","url('"+res('bg_questions.png')+"')");
    $("#game_box .q_top_left").attr("src",res('img_qustion_top_left.png'));
    $("#game_box .q_top_right").attr("src",res('img_qustion_top_right.png'));
    $("#game_box .q_bg").attr("src",res('bg_question_photo_zone.png'));
    $("#game_box .q_topic").attr("src",res('btn_qustion_q_and_a_topic.png'));
    $("#game_box .q_a_bg").attr("src",res('bg_qustion_q_and_a.png'));
    
}
function finish_res_loaded(){
    $(".finish_des_img").attr("src",res('img_final.png'));
    $(".finish_check_img").attr("src",res('btn_checkout.png'));
    $("#finish_box").css("background-image","url('"+res('bg_questions.png')+"')");
}
function result_res_loaded(){
    $(".score_master_img").attr("src",res('bg_question_photo_zone.png'));
    $(".again_play_btn,.no_play_btn").attr("src",res('btn_result.png'));
    $(".fp_logo_img").attr("src",res('img_result_fenpu.png'));
    $(".layer_small_img,.layer_big_img").attr("src",res('bg_popover_01.png'));
    $(".layer_bigger_img").attr("src",res('img_popover_download.png'));
    $("#result_box").css("background-image","url('"+res('bg_questions.png')+"')");
}
function begin(){
    $(".layer").hide();
	$(".layer_white").hide();
	$(".duang_layer").hide();
    $("#welcome_box").hide();
    $("#result_box").hide();
    $("#game_box").show();
    __begin_time = new Date().getTime();
    __curr_question = 1;
    __op_num = 0;
    show_question(__curr_question);
}
function finish(){
    __end_time = new Date().getTime();
    set_result();
    $("#game_box").hide();
    $("#finish_box").show();
    $(".finish_check_img").click(function(){
        result();
    });
    
}
function set_result(){
    var sec = parseInt((__end_time - __begin_time) /1000);
    var accuracy = __question_num / __op_num * 100;
    __user_score = accuracy + 5;
    $(".finish_time").eq(0).html("你答题用时 " + sec + " 秒正确率" + accuracy +"%");
    $(".score").html(__user_score);

    var money = 1;
    if(__user_score <50){
        money = 5;
    } else if(__user_score <50 && __user_score >200){
        money = 15;
    }else{
        money = 20;
    }
    $(".score_own_ticket").html("￥"+money);
}
function result(){
    $("#finish_box").hide();
    $("#result_box").show();
}
function resize_game_screen(){
    var screen_width = $(window).width();
    var screen_height = $(window).height();
    if(screen_width>680){
        $(".scene").width(680);
    }
    $(".scene").height(screen_height);
    $("#loading_box h2").height(screen_height);
    $("#loading_box h2").css("line-height",screen_height+"px");
}

function answer(question_id,liobj){
    if(!__can_answer){
        return;
    }
    __can_answer = false;
    liobj = $(liobj);
    var index = question_id-1;
    var question = __question_list[index];
    var answer = question.answer + "";
    var wrong_icon = "<img class='i_wrong' src='"+res('icon_question_q_and_a_wrong.png')+"' />";
    var right_icon = "<img class='i_right' src='"+res('icon_question_q_and_a_right.png')+"' />";
    __op_num ++ ;
    $(".i_right").remove();
    $(".i_wrong").remove();
    finish();
    if(liobj.index() == answer){
        var next_question_id = question_id+1;
        $(liobj).html($(liobj).html()+right_icon);
        if(next_question_id >=__question_num){
            setTimeout("finish();",300);
        }else{
            setTimeout("show_question("+next_question_id+");",300);
        }
    }else{
        $(liobj).html($(liobj).html()+wrong_icon);
        __can_answer = true;
    }
}
function show_question(question_id){
    __can_answer = true;
    var index = question_id-1;
    var question = __question_list[index];
    var pa_num = index;
    var q_num = question_id;
    if(pa_num<10){
        pa_num = "0"+pa_num;
    }
    if(q_num<10){
        q_num = "0"+q_num;
    }
    $("#game_box .q_pic").attr("src", question.pic );
    $("#game_box .q_progress").attr("src",res('img_progressbar_'+pa_num+'.png'));
    $("#game_box .q_num").attr("src",res('icon_question_num_'+q_num+'.png'));
    var answer_html = "<li class='question'>" + question.title + "</li>";
    var answer_list = question.answerList;
    for (var i=0;i<answer_list.length;i++){
        var _answer = answer_list[i];
        answer_html += "<li>" + String.fromCharCode(65+i) + ":" + _answer.text + "</li>";
    }
    $("#game_box .qa").html(answer_html);
    $("#game_box .qa").attr("question_id",question_id);
    $("#game_box .qa li:gt(0)").click(function(){
        answer(question_id,$(this));
    });
}
function load_question(){
    //ajax异步加载题库
    //将题库列表返回
    var data=[];
    for (var i=0;i<15;i++){
        data.push({
            "pic": res('pic_1.png'),
            "questionId":i,
            "title":"这个产品叫啥子"+i,
            "answerList":[
                {"text":"金吒1"},{"text":"木吒2"},{"text":"火吒3"},{"text":"土吒4"}
            ],
            "answer":1
        });
    }
    question_loaded(data);
}

$(document).ready(function(){
    resize_game_screen();
    $(window).resize(function(){
        resize_game_screen();
    }); 
    $("#welcome_box .go").click(function(){
        begin();
    });
    $(".again_play_btn,.again_play").click(function(){
      $(".layer").show();
	  $(".layer_white").show();
	  $(".duang_layer").show();
      setTimeout(function() {  
        begin();
      }, 3000);
   });
   $(".no_play_btn,.no_play").click(function(){
      $(".layer").show();
	  $(".layer_white").show();
	  $(".get_layer").show();
   });
   $(".layer").click(function(){
      $(".layer").hide();
      $(".duang_layer").hide()
      $(".get_layer").hide();
      $(".download_layer").hide();
   });
   $(".fast_get_section").click(function(){
       $.get_data(
         get_get_cash_coupon_api(),
         "score="+__user_score,
         function(data){
           if(data.error != undefined && data.error == 0){
              $(".get_layer").hide();
              $(".download_layer").show();
           }else if(data.error && data.error == 1){
              alert(data.errorString);
           }else if(data.error && data.error == 2){
              window.location=data.authuri;
           }
         },
         function(){},'json'
       );
       $(".exit_btn").click();
       setTimeout(function(){$(".cart-pop").fadeOut("slow");},1300);
     });
   
   setTimeout(function() {  
        window.scrollTo(0, 1)  ;
   }, 300); 
   jQuery.imageLoader(welcome_scene_resources,welcome_res_loaded);
   load_question();
   jQuery.imageLoader(game_scene_resources,game_res_loaded);
   jQuery.imageLoader(finish_scene_resources,finish_res_loaded);
   jQuery.imageLoader(result_scene_resources,result_res_loaded);
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
                console.log("XmlHttpRequest status: [404] \nThe requested URL was not found on this server.");
                break;
            case 500:
                console.log("XmlHttpRequest status: [500] Service Unavailable");
                break;
            case 400:
                console.log("XmlHttpRequest status: [400] Bad Request");
                break;
            case 503: // Service Unavailable
                console.log("XmlHttpRequest status: [503] Service Unavailable");
                break;
            default:
                break;
        }
    }
});

