;( function( $, window, undefined ) {
    
    'use strict';

    var $event = $.event,
    $special,
    resizeTimeout;

    // global
    var $window = $( window ),
        $document = $( document ),
        Modernizr = window.Modernizr;

    $.SparseGrafico = function( options, element ) {
        this.$elWrapper = $(element);
        this._init( options );
    };

    $.SparseGrafico.defaults = {
        // elemento contendor donde se pondra el grafico.
        contenedor: ".contenedor-grafico", 
        // id del grafico.
        id: "grafico-linea", 
        // clases extras para el grafico.
        clases: "", 
        // titulo del box que contiene el grafico.
        titulo: "Grafico",
        // parametro con los datos para el grafico chartjs.
        chartjs: {},
        // parametro con los datos para el grafico flot.
        flot: { params: {}, data: [] },
        // altura en px para el grafico.
        altura: '300px',
        // altura-maxima en px para el grafico.
        altura_maxima: '300px',
        // indica si se debe agregar el grafico dentro de un box.
        caja: true,
        // indica si se debe agregar el grafico al elemento contenedor (de lo contrario  
        // borra su contenido y agrega el grafico).
        agregar: true, 
    };

    $.SparseGrafico.prototype = {
        _init : function( options ) {
            // options
            this.options = $.extend( true, {}, $.SparseGrafico.defaults, options );

            this.agregarElemento(this.elemento());
            this.cargar();
        },

        elemento: function() {
            var grafico = "";

            if ( this.options.caja ) {
            grafico +=   '<div class="grafico ' + this.options.clases + '">\
                               <div class="box box-primary">\
                                    <div class="box-header with-border">\
                                        <h5 class="box-title">' + this.options.titulo + '</h5>\
                                    </div>\
                                    <div class="box-body chart-responsive">';
            }
            if ( !$.isEmptyObject(this.options.chartjs) ) {
                grafico += '<canvas id="' + this.options.id + '"  max-height="' + this.options.altura_maxima + '" height="' + this.options.altura + '" ></canvas>';
            } else if ( !$.isEmptyObject(this.options.flot.params) ) {
                grafico += '<div id="' + this.options.id + '" class="flot-chart"   max-height="' + this.options.altura_maxima + '"  style="height: ' + this.options.altura + ';"></div>';
            }

            if ( this.options.caja ) {
                grafico += '</div></div></div>'; // etiquetas de cierre del box.
            }

            return grafico;
        },

        agregarElemento: function( grafico ) {
            if ($("#"+this.options.id).length == 0) {
                if ( this.options.agregar ) {
                    $(this.$elWrapper).append(grafico);
                } else {
                    $(this.$elWrapper).html(grafico);
                }
            }
        },

        cargar: function() {
            this.$grafico = $("#" + this.options.id);
            this.$padreGrafico = this.$grafico.parent();
            this.graficoOriginal = this.$padreGrafico.html();

            if ( !$.isEmptyObject(this.options.chartjs) ) {
                new Chart($("#" + this.options.id)[0].getContext("2d"), this.options.chartjs);
            }
            else if ( !$.isEmptyObject(this.options.flot.params) ) {
                $.plot($("#" + this.options.id), this.options.flot.data, this.options.flot.params);
            }
        },

        recargar: function(params = {}) {   
            this.$padreGrafico.html("");
            this.$padreGrafico.append(this.graficoOriginal);
            this._init(params);
        },
    };

    var logError = function( message ) {

        if ( window.console ) {

            window.console.error( message );
        
        }

    };

    $.fn.sparseGrafico = function( options ) {
        var self = $.data( this, 'sparseGrafico' );

        if ( typeof options === 'string' ) {
            
            var args = Array.prototype.slice.call( arguments, 1 );
            
            this.each(function() {
            
                if ( !self ) {

                    logError( "cannot call methods on sparseGrafico prior to initialization; " +
                    "attempted to call method '" + options + "'" );
                    return;
                
                }
                
                if ( !$.isFunction( self[options] ) || options.charAt(0) === "_" ) {

                    logError( "no such method '" + options + "' for sparseGrafico self" );
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

                    self = $.data( this, 'sparseGrafico', new $.SparseGrafico( options, this ) );
                
                }

            });
        
        }
        
        return self;
    };

} )( jQuery, window );

function callbackLabelDonaConPorcentaje (tooltipItem, data){
    meta_datos = data.datasets[0]._meta[Object.keys(data.datasets[0]._meta)[0]].data
    total_parcial = 0
    for (var i = 0; i < meta_datos.length; i++) {
      if (!meta_datos[i].hidden){
          total_parcial += data.datasets[meta_datos[i]._datasetIndex].data[meta_datos[i]._index]
      }
    };
    valor_actual = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
    porcentaje = (valor_actual*100)/total_parcial;
      return data.labels[tooltipItem.index]+': '+Number(porcentaje.toFixed(2)).toLocaleString()+' %';
}


function callbackLabelAreaFormatoNumero(tooltipItem, data){
  return data.datasets[tooltipItem.datasetIndex].label+': '+Number(tooltipItem.yLabel.toFixed(2)).toLocaleString();
}