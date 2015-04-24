
jQuery.imageLoader = function(images,callback) {
        var total_count = 999;
        var current_count = 0;
        var finished = false;
        function __loaded(){
            current_count ++;
            if(current_count>=total_count && !finished){
                finished = true;
                callback();
            }
        }
        
        function __load_image(url) { 
            var img = new Image(); 
            img.src = url; 
            if (img.complete) {
                __loaded();
                return; 
            } 
            img.onload = function () { 
                __loaded();
            }; 
        }; 

        function __init() {
            if(!images)
                return;
            if(images instanceof Array){
                total_count = images.length;
                for(var i=0;i<images.length;i++){
                   __load_image(images[i]);
                }
            }else{
                total_count = 1;
                __load_image(images);
            }
        }
        __init();
        
}

