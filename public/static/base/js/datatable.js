;(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory(require('jquery')) :
    typeof define === 'function' && define.amd ? define(['jquery'], factory) :
    global.sparseDataTable = factory(global.jQuery)
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
    var _sparseDataTable = {
        params: {
            url : "/common/datatable/", // url que procesara la peticion ajax.
            metodo: "POST", // metodo con que se pasaran los datos.
            ajaxData: {
                id: "idTabla",
                clases: "",
                titulo: "Tabla",
            }, // datos que seran pasados a la url que procesara la peticion.
            data: [], // datos que seran pasados a la url que procesara la peticion.
            columnas: [],
            buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
            selector: ".dataTable", // selector para obtener el datatable.
            "lenguaje": {
                "url": '/static/plugins/datatables/extensions/i18n/spanish.json',
                "decimal": ",",
                "thousands": ".",
            },
            "lengthMenu": [[10, 20, 50, 100, -1], [10, 20, 50, 100, "Todo"]],
            "order": [[ 0, "asc" ]],
            "initComplete": function(settings, json) {},
            agregar: true, // indica si la tabla debe agregarse al elemento selector.
        },

        $tabla: null, // objecto dataTable.
        $dataTable: null, // objecto dataTable.
        tablaOriginal: null, // copia de la tabla antes de ser inicia por el dataTable.
        $padreTabla: null,

        iniciar: function (params = {}) {
            $.extend(this.params, params);
            this.$padreTabla = $(this.params.selector).parent();
            this.tablaOriginal = this.$padreTabla.html();

            $.ajax({
                async: false,
                url : this.params.url, // the endpoint
                type : this.params.metodo, // http method
                data : this.params.ajaxData, // data sent with the post request
                context : this, // hacemos el objeto accesible desde las funciones de ajax.
                // handle a successful response
                success : function(json) {
                    var datos = this.params.data, columnas = this.params.columnas;

                    if (this.params.data.length > 0) {
                        if (this.params.agregar) {
                            $(this.params.selector).append(json);
                        } else {
                            $(this.params.selector).html(json);
                        }
                    } else {
                        datos = json.data;
                        columnas = json.columnas;
                    }
                    this.$tabla = $("#" + this.params.ajaxData.id);
                    console.log(this.$tabla);

                    this.$dataTable = this.$tabla.DataTable({
                        data: datos,
                        responsive: true,
                        language: this.params.lenguaje,
                        columns: columnas,
                        dom: 'Blfrtip',
                        buttons: this.params.buttons,
                        "lengthMenu": this.params.lengthMenu,
                        "order": this.params.order,
                        "initComplete": this.params.initComplete,
                    });
                    // $($.fn.dataTable.tables(true)).DataTable().columns.adjust().responsive.recalc();
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

        recargar: function(params = {}) {
            this.$padreTabla.html("");
            this.$padreTabla.append(this.tablaOriginal);
            this.iniciar(params);
        }
    };
    
    return _sparseDataTable;
}));