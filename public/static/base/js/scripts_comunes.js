function irAURL(url){
    location.href=url;
    location.replace(url);
    window.location.replace(''+url);
    window.location.href = url;
}

//block page for ajax calls
/*
function blockpage(p1){
    if(p1){
        if (($('.block-page')[0]==undefined)) {
            $('body').append('<div class="block-page"></div>');
            $('body').append('<div class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></div>');
        }
    }else{
        $('.block-page').remove();
        $('.glyphicon-refresh-animate').remove();
    }
}
*/