var cliente_actual = null
var tipo_y_alojamientos = null//[{alojamientos:[{id,codigo},{}],tipoalojamiento:{nombre,id} },{}]
var canales_venta = null
var tarifas = null
var datos_habitacion = null
var cuenta_seleccionada = null
var reserva_actual = []


function ajaxConsultarCliente (cliente, url_gestion_cliente){
    datos_ajax = {
        opcion:'CONSULTA',
        cliente:cliente
    };
    var data = {
        'datos': JSON.stringify(datos_ajax)
    };
    blockpage(true)
    $.ajax({
        method: "POST",
        url: url_gestion_cliente,
        data: data
    }).done(function( response ) {
        if (response.state == 'success'){
            cliente_actual = {
                'id':response.cliente.id,
                'nombre_completo':response.cliente.nombres+' '+response.cliente.apellidos,
                'rut':response.cliente.rut+' '+response.cliente.digito_verificador,
                'empresas_asociadas': response.cliente.empresas_asociadas,
            }
            mostrarIngresoAlojamiento ();
            // $("div[name=reservando_alojamiento]").css('display','none')
            // $("#ingreso_alojamiento").css('display','block');
            // var targetOffset = $("#ingreso_alojamiento").offset().top - 100;
            // $("#ingreso_alojamiento").find('#nombre_cliente').text(  cliente_actual.nombre_completo+'['+cliente_actual.rut+']')
            // texto_empresas = ''
            // if (cliente_actual.empresas_asociadas.length > 0){
            //   texto_empresas = 'Asociado a:'
            //   for (var i = 0; i < cliente_actual.empresas_asociadas.length; i++) {
            //     if (i!=0)
            //       texto_empresas += ', '
            //     texto_empresas += cliente_actual.empresas_asociadas[i].nombre
            //   };
            // }
            // $("#ingreso_alojamiento").find('h5').text( texto_empresas)
        }
        else
            swal({
              title: "Mensaje",
              text: response.messages[0].text,
              icon: response.messages[0].type,
            });
    }).fail(function(response) {
        console.log(response);
        swal({
              title: "Servidor",
              text: "Error en la petición",
              icon: "error",
        });
    }).complete(function(){
        blockpage(false);
    });
}

function ajaxCargarOcupacionAlojamiento(url_data_ocupacion_alojamiento){
      $.ajax({
          method: "POST",
          url: url_data_ocupacion_alojamiento,
          data: {}
      }).done(function( response ) {
          console.log(response);
          if (response.state == 'success'){
              loadTimeline(response.grupos, response.items)
              loadComboBoxAlojamiento(response.info_alojamientos)
              tipo_y_alojamientos= response.info_alojamientos
          }
          else
              swal({
                title: "Información",
                text: response.messages[0].text,
                icon: response.messages[0].state
              });
      }).fail(function(response) {
          console.log(response);
          swal({
                title: "Servidor",
                text: "Error en la petición",
                icon: "error"
          });
      });
  }

  function ajaxCargarComentarios(url_comentarios){
      $.ajax({
          method: "POST",
          url: url_comentarios,
          data: {}
      }).done(function( response ) {
          console.log(response);
          if (response.state == 'success'){
              loadMultiSelectComentarios(response.comentarios)
          }
          else
              swal({
                title: "Información",
                text: response.messages[0].text,
                icon: response.messages[0].state
              });
      }).fail(function(response) {
          console.log(response);
          swal({
                title: "Servidor",
                text: "Error en la petición",
                icon: "error"
          });
      });
  }

  function ajaxCargarCanalesVenta(url_canalesventa){
      $.ajax({
          method: "POST",
          url: url_canalesventa,
          data: {}
      }).done(function( response ) {
          if (response.state == 'success'){
              canales_venta = response.canales
              loadComboBoxCanalesVenta(canales_venta)
          }
          else
              swal({
                title: "Información",
                text: response.messages[0].text,
                icon: response.messages[0].state
              });
      }).fail(function(response) {
          swal({
                title: "Servidor",
                text: "Error en la petición - Problemas al cargar los canales de venta",
                icon: "error"
          });
      });
  }


  function ajaxCargarTarifas(url_tarifas){
      $.ajax({
          method: "POST",
          url: url_tarifas,
          data: {}
      }).done(function( response ) {
          if (response.state == 'success'){
              tarifas = response.tarifas
              cargarTarifas(tarifas)
          }
          else
              swal({
                title: "Información",
                text: response.messages[0].text,
                icon: response.messages[0].state
              });
      }).fail(function(response) {
          swal({
                title: "Servidor",
                text: "Error en la petición - Problemas al cargar las tarifas de alojamientos",
                icon: "error"
          });
      });
  }


  function ajaxComprobacionOcupacion(url_comprobarocupacion, datos){
      $.ajax({
          method: "POST",
          url: url_comprobarocupacion,
          data: {datos: JSON.stringify(datos)},
      }).done(function( response ) {
          if (response.state == 'success'){
            mostrarModalResumenHabitacion();
          }
          else
              swal({
                title: "Información",
                text: response.messages[0].text,
                icon: response.messages[0].state
              });
      }).fail(function(response) {
          swal({
                title: "Servidor",
                text: "Error en la petición - Problemas al comprobar la ocupación.",
                icon: "error"
          });
      });
  }

  function ajaxCrearReserva(url_crear_reserva, datos){
      $.ajax({
          method: "POST",
          url: url_crear_reserva,
          data: {datos: JSON.stringify(datos)},
      }).done(function( response ) {
          if (response.state == 'success'){
            swal({
                title: "Reserva - R_"+response.reserva,
                text: 'La reserva ha sido ingresada exitosamente.',
                icon: 'success',
              });
              ajaxCargarOcupacionAlojamiento(url_data_ocupacion_alojamiento);
              limpiarTodo()
          }
          else
              swal({
                title: "Información",
                text: response.messages[0].text,
                icon: response.messages[0].state
              });
      }).fail(function(response) {
          swal({
                title: "Servidor",
                text: "Error en la petición - Problemas al comprobar la ocupación.",
                icon: "error"
          });
      });
  }

//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------
//     Funciones logicas
//----------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------

  function cargarTarifas(tarifas, cliente_actual=null){
    columnas = [
        {'title':'', 'data':'acciones'},
        {'title':'ID', 'data':'id'},
        {'title':'Nombre', 'data':'nombre'},
        {'title':'Descripción', 'data':'descripcion'},
        {'title':'Valores X persona', 'data':'valores'},
        {'title':'Restricciones', 'data':'restricciones', 'width':'500px'},
        {'title':'Habilitado', 'data':'habilitado'},
        {'title':'Acciones', 'data':'acciones'},
    ]

    data_table = []
    for (var q = 0; q < tarifas.length; q++) {
        item = tarifas[q]
        aux = {}
        aux['id'] = item.id
        aux['nombre'] = item.nombre
        aux['nombre'] += '<br /><span style="color:white;">-----------------------------------------------</span>'
        aux['descripcion'] = item.descripcion
        aux['habilitado'] = '<i class="material-icons text-green">check</i>'
        if (!item.habilitado)
            aux['habilitado'] = '<i class="material-icons text-red">clear</i>'
        aux['valores']= ''
        dias = [2, 3, 4, 5, 6, 7, 1]
        nombre_dias = ['---','Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        if (item.id == item.id){
            thead = ''
            tbody = ''
            i=0
            while (i <= 7){
                j=0
                while (j <= 10){
                    if (i== 0 && j==0)
                        thead += '<th></th>'
                    else
                    if (i == 0)
                        thead += '<th>'+j+'</th>'
                    else
                    if (j == 0)
                        tbody += '<tr><th>'+nombre_dias[i]+'</th>'
                    else{
                        if (j in item.valores[i])
                            tbody += '<td>'+item.valores[i][j]+'</td>'
                        else
                            tbody += '<td>---</td>'
                    }
                    j+=1
                }
                tbody += '</tr>'
                i+=1
            }
            aux['valores'] += '<table>'
            aux['valores'] += '<thead>'
            aux['valores'] += thead
            aux['valores'] += '</thead>'
            aux['valores'] += '<tbody>'
            aux['valores'] += tbody
            aux['valores'] += '</tbody>'
            aux['valores'] += '</table>'
        }
        aux['restricciones'] = ''
        aux['restricciones'] += '<strong>Temporadas:</strong>'
        for (var h = 0; h < item.restricciones.temporadas.length; h++) {
            aux['restricciones'] += item.restricciones.temporadas[h].nombre+','
        };
        aux['restricciones'] += '<br />'
        aux['restricciones'] += '<strong>Tipo de alojamiento:</strong>'
        for (var h = 0; h < item.restricciones.tipos_alojamiento.length; h++) {
            aux['restricciones'] += item.restricciones.tipos_alojamiento[h].nombre+','
        };
        aux['restricciones'] += '<br />'
        aux['restricciones'] += '<strong>Empresas:</strong>'
        for (var h = 0; h < item.restricciones.empresas.length; h++) {
            aux['restricciones'] += item.restricciones.empresas[h].nombre+','
        };
        aux['restricciones'] += '<br />'
        aux['restricciones'] += '<strong>Canales de venta:</strong>'
        for (var h = 0; h < item.restricciones.canales_venta.length; h++) {
            aux['restricciones'] += item.restricciones.canales_venta[h].nombre+','
        };
        aux['restricciones'] += '<br />'
        aux['restricciones'] += '<span style="color:white;">------------------------------------------------------------------------</span>'
        aux['acciones'] = '<button name="seleccion_tarifa" tarifa_id="'+item.id+'" tarifa_nombre="'+item.nombre+'" class="btn bg-indigo nav-pill waves-effect waves-block toggled"><i class="material-icons">flash_on</i></button>'
        data_table.push(aux)
    };
    params_tarifa.columnas = columnas
    params_tarifa.data = data_table
    if (sparseTabla_tarifa == null)
        sparseTabla_tarifa = $('#container_tabla_tarifa').sparseDataTable(params_tarifa)
    else
        sparseTabla_tarifa.recargar(params_tarifa)
  }


  function comprobarDatosHabitacion(comprobar_tarifa = false){
    if ($('#select_alojamientos option:selected').attr('alojamiento_id') == '-1'){
        swal({
            title: "Información",
            text: 'Se debe seleccionar una habitación.',
            icon: 'info',
          });
        return false
    }
    alojamiento_id = $('#select_alojamientos option:selected').attr('alojamiento_id')
    if ($('#select_personas option:selected').attr('value') == '-1'){
        swal({
            title: "Información",
            text: 'Se debe seleccionar el número de personas del alojamiento.',
            icon: 'info',
          });
        return false
    }
    if ($('#select_canal_venta option:selected').attr('canal_id') == '-1'){
        swal({
            title: "Información",
            text: 'Se debe seleccionar un canal de venta',
            icon: 'info',
          });
        return false
    }
    fecha_inicial = null
    if ($('input[name=fecha_inicial]') != null && $('input[name=fecha_inicial]').length > 0) 
      fecha_inicial = datepicker_fecha_inicial.data('plugin_bootstrapMaterialDatePicker').currentDate
    fecha_final = null
    if ($('input[name=fecha_final]') != null && $('input[name=fecha_final]').length > 0)
      fecha_final = datepicker_fecha_final.data('plugin_bootstrapMaterialDatePicker').currentDate 
    if (fecha_inicial == null){
        swal({
            title: "Información",
            text: 'Se debe seleccionar una fecha inicial.',
            icon: 'info',
          });
        return false
    }
    if (fecha_final == null){
        swal({
            title: "Información",
            text: 'Se debe seleccionar una fecha final.',
            icon: 'info',
          });
        return false
    }
    if (fecha_final < fecha_inicial){
        swal({
            title: "Información",
            text: 'La fecha final debe ser mayor o igual a la inicial.',
            icon: 'info',
          });
        return false
    }
    if (choqueFechaAlojamientoReservada (alojamiento_id, fecha_inicial, fecha_final)){
        swal({
            title: "Información",
            text: 'El alojamiento tiene conflicto de fechas, con un alojamiento selecionado. ',
            icon: 'info',
          });
        return false
    }

    if (comprobar_tarifa && $("#tarifa_seleccionada").attr('tarifa_id') == undefined || $("#tarifa_seleccionada").attr('tarifa_id') == -1){
        swal({
            title: "Información",
            text: 'No se ha seleccionado una tarifa.',
            icon: 'info',
          });
        return false
    }
    return true;
  }

function choqueFechaAlojamientoReservada (alojamiento_id, fecha_inicial, fecha_final){
  for (var i = 0; i < reserva_actual.length; i++) {
      if (reserva_actual[i].data.alojamiento_id == alojamiento_id){
        if ( fecha_inicial <= reserva_actual[i]._meta.fecha_inicial && reserva_actual[i]._meta.fecha_inicial <= fecha_final )
          return true
        if ( fecha_inicial <= reserva_actual[i]._meta.fecha_final && reserva_actual[i]._meta.fecha_final <= fecha_final )
          return true
        if ( reserva_actual[i]._meta.fecha_inicial <= fecha_inicial && fecha_inicial <= reserva_actual[i]._meta.fecha_final )
          return true
        if ( reserva_actual[i]._meta.fecha_inicial <= fecha_final && fecha_final <= reserva_actual[i]._meta.fecha_final )
          return true
        if ( fecha_inicial <= reserva_actual[i]._meta.fecha_inicial && reserva_actual[i]._meta.fecha_inicial <= fecha_final )
          return true
        if ( fecha_inicial <= reserva_actual[i]._meta.fecha_final && reserva_actual[i]._meta.fecha_final <= fecha_final)
          return true
        if (reserva_actual[i]._meta.fecha_inicial<= fecha_inicial && fecha_inicial <= reserva_actual[i]._meta.fecha_final  )
          return true
      }
  };
  return false
}

function loadTimeline(grupos, items){
      var container = document.getElementById('visualization');
      padre = container.parentNode
      padre.innerHTML = ''
      var container = document.createElement("div");
      container.setAttribute('id','visualization')
      padre.appendChild(container);
      var options = {
        orientation: {axis: 'both'},
        locale: 'es',
        // stack: true,
        groupOrder: 'content',  // groupOrder can be a property name or a sorting function
        start: moment().subtract(1, 'days').toDate(),
        end: moment().add(31, 'days').toDate(),
      };
      var dataset_grupos= new vis.DataSet();
      for (var i = 0; i < grupos.length; i++) 
        dataset_grupos.add(grupos[i])
      var dataset_items= new vis.DataSet();
      for (var i = 0; i < items.length; i++) {
        dataset_items.add(items[i])
        // console.log(items[i])
      }

      timeline = null
      timeline = new vis.Timeline(container, dataset_items, dataset_grupos, options);
      timeline.on('click', function (properties) {
        if (properties.what == 'item'){
          // console.log(properties)
          // mostrarReservaSeleccionada($($(p)[0].event.target).attr('reserva_id'))
        }
        else{
          mostrarReservaSeleccionada(null)
        }
            // alert ('click'+properties.item);
        // console.log(properties)
      });

  }

  function mostrarFechaTimeLine(fecha_inicial, fecha_final) {
    // fecha_inicial = moment(); 
    // fecha_final = moment().add(31, 'days'); 
    // mostrarFechaTimeLine(fecha_inicial.format('YYYY-MM-DD'), fecha_final.format('YYYY-MM-DD'))
    // timeline.setWindow('2014-01-01', '2014-04-01');
    timeline.setWindow(fecha_inicial, fecha_final);
  };

  function loadComboBoxAlojamiento(info){
      var select = document.createElement('select')
      var option_default = document.createElement('option')
      option_default.setAttribute('alojamiento_id','-1')
      option_default.setAttribute('value','-1')
      option_default.innerHTML = 'Seleccionar'
      select.appendChild(option_default);
      for (var i = 0; i < info.length; i++) {
            var optgroup = document.createElement('optgroup');
            optgroup.setAttribute('tipoalojamiento_id',info[i].tipoalojamiento.id)
            optgroup.setAttribute('tipoalojamiento_nombre',info[i].tipoalojamiento.nombre)
            optgroup.label = info[i].tipoalojamiento.nombre
            for (var j = 0; j < info[i].alojamientos.length; j++) {
              console.log(info[i].alojamientos[j])
                var option = document.createElement('option')
                option.setAttribute('alojamiento_id',info[i].alojamientos[j].id)
                option.setAttribute('value',info[i].alojamientos[j].id)
                option.setAttribute('codigo',info[i].alojamientos[j].codigo)
                option.innerHTML = info[i].alojamientos[j].codigo
                optgroup.appendChild(option);
            }
            select.appendChild(optgroup);
      }
      //select.setAttribute('class','selectpicker')
      document.getElementById('select_alojamientos').appendChild(select);
      select_alojamientos = $(select).selectpicker({
        width:"100%",
        showTick:true,
      });
  }

  function loadComboBoxCanalesVenta(info){
      var select = document.createElement('select')
      var option = document.createElement('option')
      option.setAttribute('canal_id','-1')
      option.setAttribute('value','-1')
      option.setAttribute('canal_nombre','-1')
      option.innerHTML = 'Seleccionar'
      select.appendChild(option);
      for (var j = 0; j < info.length; j++) {
          if (info[j].habilitado){
            var option = document.createElement('option')
            option.setAttribute('canal_id',info[j].id)
            option.setAttribute('value',info[j].id)
            option.setAttribute('canal_nombre',info[j].nombre)
            option.innerHTML = info[j].nombre
            select.appendChild(option);
          }
      }
      //select.setAttribute('class','selectpicker')
      document.getElementById('select_canal_venta').appendChild(select);
      select_canal_venta =  $(select).selectpicker({
        showTick:true,
        width:"100%",
      });
  }


  function loadMultiSelectComentarios(info){
      var select = document.createElement('select')
      select.setAttribute('id','select_comentarios')
      select.setAttribute('multiple','multiple')
      // select.setAttribute('name',"select_comentarios[]")
      select.setAttribute('class',"ms")
      var option = document.createElement('option')
      for (var j = 0; j < info.length; j++) {
          var option = document.createElement('option')
          option.setAttribute('texto',info[j].texto)
          option.setAttribute('value',info[j].id)
          option.innerHTML = info[j].texto
          select.appendChild(option);
      }
      document.getElementById('div_select_comentarios').appendChild(select);
      select_comentarios =  $(select).multiSelect({
          selectableHeader: "<div >Ingresar comentarios al alojamiento:</div>",
          selectionHeader: "<div >Comentarios:</div>",
          // selectableFooter: "<div class='custom-header'>Selectable footer</div>",
          // selectionFooter: "<div class='custom-header'>Selection footer</div>"
        });
  }


  function generarItemResera(){
     var item = {
        data:{},
        _meta:{},
     }
     var flag= false
     for (var i = 0; i < tipo_y_alojamientos.length && !flag; i++) {
        tipo_y_alojamientos[i]
        for (var j = 0; j < tipo_y_alojamientos[i].alojamientos.length; j++) {
            if (tipo_y_alojamientos[i].alojamientos[j].id == datos_habitacion.alojamiento_id){
              flag = true
              item.data.alojamiento_id = datos_habitacion.alojamiento_id
              item._meta.alojamiento_codigo = tipo_y_alojamientos[i].alojamientos[j].codigo
              item._meta.tipoalojamiento_nombre = tipo_y_alojamientos[i].tipoalojamiento.nombre
            }
        };
     };
     flag= false
     item.data.cliente = cliente_actual.id
     item.data.numero_personas = datos_habitacion.numero_personas
     item.data.fecha_inicial = datos_habitacion.fecha_inicial
     item.data.fecha_final = datos_habitacion.fecha_final
     item._meta.fecha_inicial = moment(datos_habitacion.fecha_inicial, 'YYYY-MM-DD', true); 
     item._meta.fecha_final = moment(datos_habitacion.fecha_final, 'YYYY-MM-DD', true); 

     for (var i = 0; i < canales_venta.length && !flag; i++) {
        if (canales_venta[i].id == datos_habitacion.canal_venta){
          flag = true
          item.data.canal_venta = canales_venta[i].id
          item._meta.canalventa_nombre = canales_venta[i].nombre
        }
     };
     item.data.cautiva = datos_habitacion.cautiva
     item._meta.cautiva = item.data.cautiva ? 'SI' : 'NO'

     flag= false
     tarifa_actual = null
     for (var i = 0; i < tarifas.length && !flag; i++) {
        if (tarifas[i].id == datos_habitacion.tarifa){
          flag = true
          item.data.tarifa = tarifas[i].id
          item._meta.tarifa_nombre = tarifas[i].nombre
          tarifa_actual = tarifas[i]
        }
     };

     aux = moment(datos_habitacion.fecha_inicial); 
     item._meta.detalle_valores = []
     item._meta.total = 0
     while (aux <= item._meta.fecha_final){
        dow = aux.isoWeekday() % 7 + 1
        aux_valor = tarifa_actual.valores[dow][datos_habitacion.numero_personas]
         item._meta.detalle_valores.push({
             dow: dow,
             fecha:aux.format('dddd DD MMMM YYYY'),
             valor:aux_valor
         })
         aux.add(1, 'day')
         item._meta.total += aux_valor
      }
    item._meta.comentarios = datos_habitacion.comentarios
    item.data.comentarios = ''
    for (var i = 0; i < datos_habitacion.comentarios.length; i++) {
      if (i!=0)
        item.data.comentarios += ', '
      item.data.comentarios += datos_habitacion.comentarios[i].texto
    };
     return item
  }

  function eliminarAlojamientoDeReserva(id){
      aux_reservas = []
      for (var i = 0; i < reserva_actual.length; i++) 
        if (i != id)
          aux_reservas.push(reserva_actual[i])
      reserva_actual = null
      reserva_actual = aux_reservas
  }

  function limpiarTodo(){
    cliente_actual = null
    cuenta_seleccionada = null
    reserva_actual = []
    mostrarReservaActual()
    limpiarSeccionHabitacion()
    $("div[name=reservando_alojamiento]").css('display','none')
    $("#seleccion_cliente").css('display','none')
    $("#cuenta_seleccionada").val("")
    $("#cuenta_seleccionada").attr('-1')
    $("#cuenta_seleccionada").attr('-1')
  }

  function limpiarSeccionHabitacion(){
    datos_habitacion = null
    $('input[type=checkbox]').iCheck('uncheck'); 
    select_alojamientos.selectpicker('val', '-1');
    select_canal_venta.selectpicker('val', '-1');
    select_personas.selectpicker('val', '-1');
    select_comentarios.multiSelect('deselect_all');
    datepicker_fecha_inicial.val("")
    datepicker_fecha_inicial.data('plugin_bootstrapMaterialDatePicker').currentDate = null
    datepicker_fecha_final.val("")
    datepicker_fecha_final.data('plugin_bootstrapMaterialDatePicker').currentDate = null
    $("#tarifa_seleccionada").val('')
    $("#tarifa_seleccionada").attr('tarifa_id') == -1
  }

  function mostrarIngresoAlojamiento (){
      $("div[name=reservando_alojamiento]").css('display','none')
      $("#ingreso_alojamiento").css('display','block');
      var targetOffset = $("#ingreso_alojamiento").offset().top - 100;
      $("#ingreso_alojamiento").find('#nombre_cliente').text(  cliente_actual.nombre_completo+'['+cliente_actual.rut+']')
      texto_empresas = ''
      if (cliente_actual.empresas_asociadas.length > 0){
        texto_empresas = 'Asociado a:'
        for (var i = 0; i < cliente_actual.empresas_asociadas.length; i++) {
          if (i!=0)
            texto_empresas += ', '
          texto_empresas += cliente_actual.empresas_asociadas[i].nombre
        };
      }
      $("#ingreso_alojamiento").find('h5').text( texto_empresas)
  }

  function mostrarModalResumenHabitacion(){
      reserva = generarItemResera()
      $("#modal_resumen_alojamiento").find('span[id=alojamiento]').text(reserva._meta.alojamiento_codigo)
      $("#modal_resumen_alojamiento").find('span[id=tipo]').text(reserva._meta.tipoalojamiento_nombre)
      $("#modal_resumen_alojamiento").find('span[id=personas]').text(reserva.data.numero_personas)
      $("#modal_resumen_alojamiento").find('span[id=fecha]').text(reserva._meta.fecha_inicial.format('dddd DD MMMM YYYY') +' - '+ reserva._meta.fecha_final.format('dddd DD MMMM YYYY'))
      $("#modal_resumen_alojamiento").find('span[id=canal_venta]').text(reserva._meta.canalventa_nombre)
      $("#modal_resumen_alojamiento").find('span[id=cautiva]').text(reserva._meta.cautiva)
      $("#modal_resumen_alojamiento").find('span[id=tarifa]').text(reserva._meta.tarifa_nombre)
      $("#modal_resumen_alojamiento").find('span[id=total]').text(Number(reserva._meta.total.toFixed(0)).toLocaleString())
      var detalle = ''
      for (var i = 0; i < reserva._meta.detalle_valores.length; i++) {
        if (i != 0)
          detalle +='<br />'
        detalle += '$ '+Number(reserva._meta.detalle_valores[i].valor.toFixed(0)).toLocaleString()  +' ,    '+reserva._meta.detalle_valores[i].fecha
      };
      $("#modal_resumen_alojamiento").find('span[id=detalle]').html(detalle)
    comentarios = ''
    for (var i = 0; i < reserva._meta.comentarios.length; i++) {
      if (i!=0)
        comentarios += '<br />'
      comentarios += reserva._meta.comentarios[i].texto
    };
    $("#modal_resumen_alojamiento").find('span[id=comentarios]').html(comentarios)
    $("#modal_resumen_alojamiento").modal();
  }


  function mostrarSeleccionCuenta(){
    forms_cuentas = $('div[name=grupo_seleccion_cuentas]')
    forms_cuentas.text('')
    var input_cliente = '<input name="cuenta" cuenta_tipo="persona" cuenta_id="'+cliente_actual.id+'" id="cuenta_c_'+cliente_actual.id+'" class="with-gap radio-col-yellow" type="radio" value="'+cliente_actual.id+'">\
                <label for="cuenta_c_'+cliente_actual.id+'" class="m-l-20">'+cliente_actual.nombre_completo+'</label><br />'
    forms_cuentas.append(input_cliente)
    for (var i = 0; i < cliente_actual.empresas_asociadas.length; i++) {
      cliente_actual.empresas_asociadas[i]
      var input_empresa = '<input name="cuenta" id="cuenta_e_'+cliente_actual.empresas_asociadas[i].id+'" class="with-gap radio-col-amber" type="radio" cuenta_tipo="empresa" cuenta_id="'+cliente_actual.empresas_asociadas[i].id+'" value="'+cliente_actual.empresas_asociadas[i].id+'"><label for="cuenta_e_'+cliente_actual.empresas_asociadas[i].id+'" class="m-l-20">'+cliente_actual.empresas_asociadas[i].nombre+'</label><br />';
      forms_cuentas.append(input_empresa);
    };
    $("#modal_seleccion_cuenta_cargo").modal('show')
  }

  function mostrarReservaActual(){
    tbody = $('tbody[id=body_alojamientos_seleccionadas]')
    tbody.text('')
    var total = 0;
    for (var i = 0; i < reserva_actual.length; i++) {
      var aux_comentarios = ''
      for (var k = 0; k < reserva_actual[i]._meta.comentarios.length; k++) {
          if (k != 0)
            aux_comentarios += '<br />'
          aux_comentarios += reserva_actual[i]._meta.comentarios[k].texto
      }
      var $tr = $('<tr></tr>')
      var $td = $('<td></td>')
      tbody.append( $tr.append(
          $('<td></td>').append(reserva_actual[i]._meta.alojamiento_codigo),
          [
            $('<td></td>').append(reserva_actual[i].data.numero_personas),
            $('<td></td>').append(reserva_actual[i]._meta.fecha_inicial.format('dddd DD MMMM YYYY')),
            $('<td></td>').append(reserva_actual[i]._meta.fecha_final.format('dddd DD MMMM YYYY')),
            $('<td></td>').append(reserva_actual[i]._meta.canalventa_nombre),
            $('<td></td>').append(reserva_actual[i]._meta.cautiva),
            $('<td></td>').append(aux_comentarios),
            $('<td></td>').append(reserva_actual[i]._meta.tarifa_nombre),
            $('<td></td>').append('$&nbsp;'+Number(reserva_actual[i]._meta.total.toFixed(0)).toLocaleString()),
            $('<td></td>').append('<button type="button" class="btn bg-red btn-circle waves-effect waves-circle waves-float" tipo="eliminar_alojamiento_reserva" alojamiento_id="'+i+'">\
                                    <i class="material-icons"  >clear</i>\
                                  </button>'),
          ]
      ))
      total += reserva_actual[i]._meta.total
      // reserva_actual[i]
    };
    tbody.append( $('<tr></tr>').append('\
      <td></td>\
      <td></td>\
      <td></td>\
      <td></td>\
      <td></td>\
      <td></td>\
      <td></td>\
      <th>Total Reserva:</th>\
      <td colspan="2" style="font-size: 20px;" >'+'$&nbsp;'+Number(total.toFixed(0)).toLocaleString()+'</td>\
      <!--<td></td>-->')
    )
  }


  function ingresarReserva(){
    data = {
      'cliente':cliente_actual.id,
      'reservas': [],
      'cuenta':cuenta_seleccionada
    }
    for (var i = 0; i < reserva_actual.length; i++) {
      data.reservas.push(reserva_actual[i].data)
    };
    ajaxCrearReserva(url_crear_reserva, data)
  }


  function mostrarReservaSeleccionada (reserva_id){
    $('div[name=item_ocupacion]').removeClass('custom-selected-item')
    if (reserva_id != null)
      $('div[name=item_ocupacion][reserva_id='+reserva_id+']').addClass('custom-selected-item')
  }

