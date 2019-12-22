
;( function( $, window, undefined ) {
    
    'use strict';

    var $event = $.event,
    $special,
    resizeTimeout;

    // global
    var $window = $( window ),
        $document = $( document ),
        Modernizr = window.Modernizr;

    $.SparseDataTable = function( options, element ) {
        this.$elWrapper = $(element);
        this._init( options );
    };

    $.SparseDataTable.defaults = {
        // id de la tabla.
        id : "idTabla",
        // clases adicionales a agregar a la tabla.
        clases : "",
        // titulo del box que contiene la tabla.
        titulo : "",
        // url que procesara la peticion ajax.
        url : "", 
        // datos que seran pasados a la url que procesara la peticion.
        ajaxData: {}, 
        // datos que seran pasados a la url que procesara la peticion.
        data: [], 
        // columnas de la tabla.
        columnas: [],
        // botones con las opciones para exportar la información la tabla.
        buttons: [],
        // contenedor donde se colocara el datatable en caso de usar ajax.
        setAllButtons: false,
        // contenedor donde se colocara el datatable en caso de usar ajax.
        //contenedor: ".dataTable",
        // lenguaje para tratar los datos de la tabla. 
        "lenguaje": {
            "url": '/static/plugins/datatables/extensions/i18n/spanish.json',
            "decimal": ",",
            "thousands": ".",
        },
        // opciones para mostrar la cnatidad de elementos de la tabla por pagina.
        "lengthMenu": [[10, 20, 50, 100, -1], [10, 20, 50, 100, "Todo"]],
        // orden en que se muestran los datos.
        "order": [[ 0, "asc" ]],
        // evento que se llama una vez que la tabla ha sido cargada y mostrada en la pagina.
        "initComplete": function(settings, json) {},
        // evento que se llama antes de iniciar el proceso procesar los datos.
        "preProcess": function(respuesta) { return respuesta },
        // evento que se llama una vez terminada la carga de success
        "successComplete": function(respuesta) {},
        // indica si se debe agregar el grafico dentro de un box.
        caja: true,
        // indica si la tabla debe agregarse al elemento contenedor sin sobreescribir su contenido.
        agregar: true, 
        // indica si el elemento (div) para el datatable sera obtenido desde el servidor. 
        ajax: false,
        //Indica si la petición ajax es asincrona
        async: true,
        //Indica si se debe mostrar la tabla paginada
        "paging": true,
        // indica si se debe mostrar el cuadro de busqueda
        searching:true,
        // indica si se calcula automaticamente el ancho de las columnas
        "autoWidht": true,
        // Configuración general de columnas
        columnDefs:null,
        //indica el tamaño de la tabla para scroll Y
        "scrollY":null,
        //indica si se debe setear el scroll al colapsar
        "scrollCollapse": null,
        // indeica si debe aparecer el scroll horizontal
        "scrollX": false,
    };

    $.SparseDataTable.prototype = {
        _init : function( options ) {
            // options
            this.options = $.extend( true, {}, $.SparseDataTable.defaults, options );

            if ( this.options.ajax ) {
                // Cargamos la tabla por desde la respuesta del servidor.
                this.ajax();
            } else {
                this.agregarElemento(this.elemento());
                this.cargar();
            }
        },

        cargar: function() {
            this.$tabla = $("#" + this.options.id);
            this.$padreTabla = this.$tabla.parent();
            this.tablaOriginal = this.$padreTabla.html();
            if (this.options.setAllButtons)
                this.options.buttons = ['copy', 'csv', 'excel', 'pdf', 'print']
            this.DataTable = this.$tabla.DataTable({
                data: this.options.data,
                responsive: true,
                language: this.options.lenguaje,
                columns: this.options.columnas,
                dom: 'Blfrtip',
                buttons: this.options.buttons,
                "lengthMenu": this.options.lengthMenu,
                "order": this.options.order,
                "initComplete": this.options.initComplete,
                "paging": this.options.paging,
                searching:this.options.searching,
                "autoWidth": this.options.autoWidht,
                columnDefs: this.options.columnDefs,
                "scrollY": this.options.scrollY,
                "scrollCollapse":  this.options.scrollCollapse,
                "scrollX": this.options.scrollX,
            });
        },

        ajax: function() {
            this.options.ajaxData["id"] = this.options.id;
            this.options.ajaxData["clases"] = this.options.clases;
            this.options.ajaxData["titulo"] = this.options.titulo;

            // si el elemento se agrega por ajax, se establece el template que lo renderiza.
            if ( this.options.url == "" ) {
                this.options.url = "/common/datatable/";
            }

            $.ajax({
                async: this.options.async,
                url : this.options.url, // the endpoint
                type : "POST", // http method
                data : this.options.ajaxData, // data sent with the post request
                context : this, // hacemos el objeto accesible desde las funciones de ajax.
                success : function(respuesta) {
                    respuesta = this.options.preProcess(respuesta);
                    // asignamos los datos y columnas que fueron retornados en la respuesta.
                    if ( this.options.data.length == 0 ) {
                        this.options.data = respuesta.data;
                    }

                    if ( this.options.columnas.length == 0 ) {
                        this.options.columnas = respuesta.columnas;
                    }
                    
                    // if ( respuesta.hasOwnProperty("elemento") ) {
                    //     this.agregarElemento(respuesta.elemento);
                    // }
                    
                    this.agregarElemento(this.elemento());
                    this.cargar();
                    this.options.successComplete(respuesta);
                },
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    $('.content-wrapper').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        },

        elemento: function() {
            var tabla = '<div class="tabla ' + this.options.clases +'">\
                          <div class="box box-primary">\
                            <div class="box-header with-border">\
                              <h5 class="box-title">' + this.options.titulo +'</h5>\
                            </div>\
                            <div class="box-body">\
                              <div class="table-responsive">\
                                <table id="' + this.options.id + '" class="table responsive table-hover table-striped dataTable js-exportable"></table>\
                              </div>\
                            </div>\
                          </div>\
                        </div>';

            return tabla;
        },

        agregarElemento: function( tabla ) {
            if ($("#"+this.options.id).length == 0) {
                if (this.options.agregar) {
                    $(this.$elWrapper).append(tabla);
                } else {
                    $(this.$elWrapper).html(tabla);
                }
            }
        },

        recargar: function(params = {}) {   
            this.$padreTabla.html("");
            this.$padreTabla.append(this.tablaOriginal);
            this._init(params);
        },

    };

    var logError = function( message ) {

        if ( window.console ) {

            window.console.error( message );
        
        }

    };

    $.fn.sparseDataTable = function( options ) {
        var self = $.data( this, 'sparseDataTable' );

        if ( typeof options === 'string' ) {
            
            var args = Array.prototype.slice.call( arguments, 1 );
            
            this.each(function() {
            
                if ( !self ) {

                    logError( "cannot call methods on sparseDataTable prior to initialization; " +
                    "attempted to call method '" + options + "'" );
                    return;
                
                }
                
                if ( !$.isFunction( self[options] ) || options.charAt(0) === "_" ) {

                    logError( "no such method '" + options + "' for sparseDataTable self" );
                    return;
                
                }
                
                self[ options ].apply( self, args );
            
            });
        
        } 
        else {
        
            this.each(function() {
                
                if ( self ) {

                    self._init();
                
                }
                else {

                    self = $.data( this, 'sparseDataTable', new $.SparseDataTable( options, this ) );
                
                }

            });
        
        }
        
        return self;
    };



} )( jQuery, window );