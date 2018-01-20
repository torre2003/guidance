$.validator.setDefaults({
  debug: true,
  success: "valid"
});

$(function () {
    form_validation = $('#form_validation').validate({
        success: "valid",
        rules: {
            'checkbox': {
                required: true
            },
            'gender': {
                required: true
            },
            'nombres': {
                required: true,
                minlength: 10,
                maxlength: 200,
            },
            'apellidos': {
                required: true,
                maxlength: 200,
            },
            'direccion': {
                required: true,
                maxlength: 300,
            },
            'ciudad': {
                required: true,
                maxlength: 100,
            },
            'pais': {
                required: true,
                maxlength: 100,
            },
            'telefono': {
                required: true,
                maxlength: 100,
            },
            'rut': {
                required: true,
                maxlength: 7,
                maxlength: 8,
                digits: true
            },
            'dv': {
                required: true,
                maxlength: 1,
            },
            'telefono': {
                maxlength: 300,
            },
        },
        highlight: function (input) {
            $(input).parents('.form-line').addClass('error');
        },
        unhighlight: function (input) {
            $(input).parents('.form-line').removeClass('error');
        },
        errorPlacement: function (error, element) {
            $(element).parents('.form-group').append(error);
        }
    });

    //Advanced Form Validation
    $('#form_advanced_validation').validate({
        rules: {
            'date': {
                customdate: true
            },
            'creditcard': {
                creditcard: true
            }
        },
        highlight: function (input) {
            $(input).parents('.form-line').addClass('error');
        },
        unhighlight: function (input) {
            $(input).parents('.form-line').removeClass('error');
        },
        errorPlacement: function (error, element) {
            $(element).parents('.form-group').append(error);
        }
    });

    //Custom Validations ===============================================================================
    //Date
    $.validator.addMethod('customdate', function (value, element) {
        return value.match(/^\d\d\d\d?-\d\d?-\d\d$/);
    },
        'Please enter a date in the format YYYY-MM-DD.'
    );


    //Validación de prueba
    $.validator.addMethod('nombres_aaa', function (value, element) {
        if (value=='aaa')
            return true;
        return false;
    },
        'El nombre solo puede ser aaa'
    );


    //Credit card
    $.validator.addMethod('creditcard', function (value, element) {
        return value.match(/^\d\d\d\d?-\d\d\d\d?-\d\d\d\d?-\d\d\d\d$/);
    },
        'Please enter a credit card in the format XXXX-XXXX-XXXX-XXXX.'
    );
    //==================================================================================================
});