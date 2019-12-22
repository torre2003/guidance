//Mostrar paso selección de cliente
$(document).on('click',"button[id=abrir_ingresar_reserva]" ,function() {
    // cliente_actual = null
    // reserva_actual = []
    // mostrarReservaActual()
    // limpiarSeccionHabitacion()
    limpiarTodo()
    $("div[name=reservando_alojamiento]").css('display','none')
    $("#seleccion_cliente").css('display','block')
    var targetOffset = $("#seleccion_cliente").offset().top - 100;
    $('html, body').animate({scrollTop: targetOffset },500);
    $("#tarifa_seleccionada").val('')
    setTimeout(function(){
        sparseTabla_cliente.DataTable.order( [ 1, 'asc' ] ).draw();
    }, 500);
});

//Mostrar paso ingresar reserva con cliente seleccionado
$(document).on('click',"button[name=seleccion_cliente]" ,function() {
    td_fila =$(this).parent().parent().parent().parent().parent().parent()
    // $("#ingreso_alojamiento").find('#nombre_cliente').text(  td_fila.find('.nombres').text()+' '+td_fila.find('.apellidos').text()+'['+td_fila.find('.rut').text()+']')
    ajaxConsultarCliente($(this).attr('cliente'),url_gestion_cliente)
});

$(document).on('click',"button[name=ingresar_reserva]" ,function() {
    if (reserva_actual.length == 0 ){
        swal({
          title: "Ingresar reserva",
          text: "No se han ingresado alojamientos a la reserva",
          icon: "error",
        })
    }
    else
    if (cuenta_seleccionada == null){
        swal({
          title: "Cuenta cargo",
          text: "No se han una a realizar el cargo",
          icon: "error",
        })
    }
    else{
        swal({
          title: "Confirmar ingreso reserva",
          text: "",
          icon: "info",
          buttons: ['Cancelar', 'Aceptar'],
        })
        .then((ingresar) => {
          if (ingresar) {
            ingresarReserva();
          }
        });
    }
    
    // $("#ingreso_alojamiento").css('display','block');
});

$(document).on('click',"button[name=cancelar]" ,function() {
    if (reserva_actual.length > 0 ){
        swal({
          title: "Cancelar reserva?",
          text: "Estas seguro de cancelar la reservación en proceso!",
          icon: "warning",
          buttons: ['No', 'Si'],
          dangerMode: true,
        })
        .then((cancelar) => {
          if (cancelar) {
            $("div[name=reservando_alojamiento]").css('display','none')
            cliente_actual = null
          }
        });
    }else{
        $("div[name=reservando_alojamiento]").css('display','none')
        cliente_actual = null
    }
    // $("#ingreso_alojamiento").css('display','block');
});

$(document).on('click',"button[name=abrir_seleccion_tarifa]" ,function() {
    if (comprobarDatosHabitacion()){
        $("#modal_tarifas").modal();
        setTimeout(function(){ sparseTabla_tarifa.DataTable.order( [ 1, 'asc' ] ).draw();}, 500);
        // alojamiento_id = $('#select_alojamientos option:selected').attr('alojamiento_id')
        // $('#select_personas option:selected').attr('value')
        // ($('#select_canal_venta option:selected').attr('canal_id') == '-1')
        datos_habitacion = {
            cliente:cliente_actual.id,
            alojamiento_id : $('#select_alojamientos option:selected').attr('alojamiento_id'),
            numero_personas : $('#select_personas option:selected').attr('value'),
            canal_venta : $('#select_canal_venta option:selected').attr('canal_id'),
            fecha_inicial : datepicker_fecha_inicial.data('plugin_bootstrapMaterialDatePicker').currentDate.format("YYYY-MM-DD"),
            fecha_final : datepicker_fecha_final.data('plugin_bootstrapMaterialDatePicker').currentDate.format("YYYY-MM-DD"),
        }
    }
    else{
        
    }
});

$(document).on('click',"button[name=seleccion_tarifa]" ,function() {
    $("#modal_tarifas").modal('hide');
    $("#tarifa_seleccionada").val($(this).attr('tarifa_nombre'))
    $("#tarifa_seleccionada").attr('tarifa_id',$(this).attr('tarifa_id'))
    datos_habitacion.tarifa = $(this).attr('tarifa_id')
});

$(document).on('click',"button[name=agregar_alojamiento]" ,function() {
    if (comprobarDatosHabitacion(comprobar_tarifa = true, comprobar_cuenta = true)){
        comentarios = []
        opt_comentarios = $('#select_comentarios option:selected')
        for (var i = 0; i < opt_comentarios.length; i++) {
            comentarios.push({
                id:$(opt_comentarios[i]).attr('value'),
                texto:$(opt_comentarios[i]).attr('texto'),
            })
        };
        datos_habitacion = {
            cliente:cliente_actual.id,
            alojamiento_id : $('#select_alojamientos option:selected').attr('alojamiento_id'),
            numero_personas : $('#select_personas option:selected').attr('value'),
            canal_venta : $('#select_canal_venta option:selected').attr('canal_id'),
            fecha_inicial : datepicker_fecha_inicial.data('plugin_bootstrapMaterialDatePicker').currentDate.format("YYYY-MM-DD"),
            fecha_final : datepicker_fecha_final.data('plugin_bootstrapMaterialDatePicker').currentDate.format("YYYY-MM-DD"),
            tarifa : $("#tarifa_seleccionada").attr('tarifa_id'),
            cautiva : $("input[type=checkbox]").is(':checked'),
            cuenta : {
                usuario :$("#cuenta_seleccionada").attr('cuenta_id'),
                tipo_usuario: $("#cuenta_seleccionada").attr('cuenta_tipo'),
            },
            comentarios : comentarios,
        }
        ajaxComprobacionOcupacion(url_comprobarocupacion, datos_habitacion)
    }
});

$(document).on('click',"button[name=modal_resumen_alojamiento_cancelar]" ,function() {
    $("#modal_resumen_alojamiento").modal('hide');
});

$(document).on('click',"button[name=modal_resumen_alojamiento_agregar]" ,function() {
    $("#modal_resumen_alojamiento").modal('hide');
    reserva = generarItemResera()
    reserva_actual.push(reserva)
    mostrarReservaActual()
    limpiarSeccionHabitacion()
});

$(document).on('click',"button[name=abrir_seleccion_cuenta]" ,function() {
    // $("#modal_seleccion_cuenta_cargo").modal('show');
    if (cliente_actual != null){
        mostrarSeleccionCuenta()
    }
    else{
         swal({
          title: "Error en la reserva",
          text: "Actualize la página antes de continuar.",
          icon: "Error",
        })
    }
});


$(document).on('click',"button[name=seleccion_cuenta_cargo_cancelar]" ,function() {
    $("#modal_seleccion_cuenta_cargo").modal('hide');
});


$(document).on('click',"button[name=seleccion_cuenta_cargo_agregar]" ,function() {
    radio_seleccionado = $( "input[type=radio][name=cuenta]:checked" )
    if (radio_seleccionado.length != 0){
        $("#modal_seleccion_cuenta_cargo").modal('hide');
        $("#cuenta_seleccionada").val(radio_seleccionado.next('label').text())
        $("#cuenta_seleccionada").attr('cuenta_id',radio_seleccionado.attr('cuenta_id'))
        $("#cuenta_seleccionada").attr('cuenta_tipo',radio_seleccionado.attr('cuenta_tipo'))
        cuenta_seleccionada = {
            cuenta_usuario: radio_seleccionado.attr('cuenta_id'),
            cuenta_tipo_usuario: radio_seleccionado.attr('cuenta_tipo'),
       }

    }else{
         swal({
          title: "Cuenta cargo",
          text: "Se debe seleccionar una cuenta.",
          icon: "error",
        })
    }
    
});



$(document).on('click',"button[tipo=eliminar_alojamiento_reserva]" ,function() {
    alojamiento_id = $(this).attr('alojamiento_id')
    eliminarAlojamientoDeReserva(alojamiento_id)
    mostrarReservaActual()
});


// $(document).on('click',"div[name=item_ocupacion]" ,function() {
$(document).on('click',".vis-item" ,function() {
    div_item = $(this).find("div[name=item_ocupacion]")
    if (div_item.length > 0 )
        mostrarReservaSeleccionada($(div_item).attr('reserva_id'))
    else
        mostrarReservaSeleccionada(null)
});

