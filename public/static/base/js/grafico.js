;(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory(require('jquery')) :
    typeof define === 'function' && define.amd ? define(['jquery'], factory) :
    global.sparseGrafico = factory(global.jQuery)
}(this, function ($) {
    // Codigo necesario para permitir peticiones ajax.
    $.ajaxSetup({ 
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                         if (cookie.substring(0, name.length + 1) == (name + '=')) {
                             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                             break;
                         }
                     }
                 }
                 return cookieValue;
             }
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         } 
    });

    // Inicia el datatable.
    var _sparseGrafico = {
        params: {
            tipo: "morris_area", // tipo de grafico.
            selector: ".contenedor-grafico", 
            id: "grafico-area", 
            clases: "", 
            titulo: "Grafico",
            resize: true,
            data: [],
            xkey: 'y',
            ykeys: ['item1', 'item2'],
            labels: ['Item 1', 'Item 2'],
            lineColors: ['#a0d0e0', '#3c8dbc'],
            hideHover: 'auto',
            agregar: true // indica si se debe agregar el grafico al elemento.
        },

        $el: null, // el elemento con los filtros.

        iniciar: function (params = {}) {
            $.extend(this.params, params);
            console.log(this.params);

            $.ajax({
                async: false,
                url : "/common/grafico/", // the endpoint
                type : "POST", // http method
                data : { 
                    "id": this.params.id, 
                    "clases": this.params.clases, 
                    "titulo": this.params.titulo, 
                },
                context : this, // hacemos el objeto accesible desde las funciones de ajax.
                // handle a successful response
                success : function(json) {
                    var $el = $(this.params.selector);

                    if (this.params.agregar) {
                        $el.append(json);
                    } else {
                        $el.html(json);
                    }

                    if ( this.params.tipo == "morris_area" ) {
                        var area = new Morris.Area({
                          element: this.params.id,
                          resize: this.params.reize,
                          data: this.params.data,
                          xkey: this.params.xkey,
                          ykeys: this.params.ykeys,
                          labels: this.params.labels,
                          lineColors: this.params.lineColors,
                          hideHover: this.params.hideHover
                        });
                    } else if ( this.params.tipo == "morris_linea" ) {
                        var line = new Morris.Line({
                          element: this.params.id,
                          resize: this.params.reize,
                          data: this.params.data,
                          xkey: this.params.xkey,
                          ykeys: this.params.ykeys,
                          labels: this.params.labels,
                          lineColors: this.params.lineColors,
                          hideHover: this.params.hideHover
                        });
                    } else if ( this.params.tipo == "morris_donut" ) {
                        var donut = new Morris.Donut({
                          element: this.params.id,
                          resize: this.params.reize,
                          colors: this.params.colors,
                          data: this.params.data,
                          hideHover: this.params.hideHover
                        });
                    } else if ( this.params.tipo == "morris_barra" ) {
                        var bar = new Morris.Bar({
                          element: this.params.id,
                          resize: this.params.reize,
                          data: this.params.data,
                          barColors: this.params.barColors,
                          xkey: this.params.xkey,
                          ykeys: this.params.ykeys,
                          labels: this.params.labels,
                          hideHover: this.params.hideHover
                        });
                    }
                },
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    $('.content-wrapper').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });

            return this;
        },
    };
    
    return _sparseGrafico;
}));