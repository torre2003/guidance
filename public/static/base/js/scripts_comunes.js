function irAURL(url){
    location.href=url;
    location.replace(url);
    window.location.replace(''+url);
    window.location.href = url;
}

//block page for ajax calls

function blockpage(p1){
    if(p1){
        if (($('.block-page')[0]==undefined)) {
            $('body').append('<div class="block-page"></div>');
            $('body').append('<div class="glyphicon  glyphicon-refresh-animate"><div class="preloader pl-size-xs"><div class="spinner-layer pl-yellow"><div class="circle-clipper left"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div><div class="preloader pl-size-xl"><div class="spinner-layer"><div class="circle-clipper left"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div><div class="preloader pl-size-xs"><div class="spinner-layer pl-yellow"><div class="circle-clipper left"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div></div>');
        }
    }else{
        $('.block-page').remove();
        $('.glyphicon-refresh-animate').remove();
    }
}

function removeLoadBase(){
    $('#loading_').remove();
}
/**
 * Resize function without multiple trigger
 * 
 * Usage:
 * $(window).smartresize(function(){  
 *     // code here
 * });
 */
(function($){
    $(document).ready(function() {
        var flag = true
        var a = $('div[class=menu]').find("a[href$='" + location.pathname + "']")
        a.addClass('toggled')
        var li = a.parent('li')
        var ul = null
        if (li.length == 0)
            flag = false
        while (flag){
            li.addClass('active');
            a = li.find("a:first-child")
            a.addClass('toggled')
            ul = li.parent('ul')
            if (ul.length > 0){
                ul.css({'display':'block'})
                li = ul.parent('li')
                if (li.length == 0)
                    flag = false
            }
            else
                flag = false
        }
        var activado = $('li[class=active]')
        if (activado.length == 0){
            $('li[id=index]').addClass('active');
        }
        removeLoadBase();
    })
})(jQuery);


