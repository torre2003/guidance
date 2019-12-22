
function enviarForm (form_id){
        $('form').submit();
}


/*
 * Calcula digito verificador
 */
function calculaDigitoVerificador (rut) {
    // type check
    if (!rut || !rut.length || typeof rut !== 'string') {
        return -1;
    }
    // serie numerica
    var secuencia = [2,3,4,5,6,7,2,3];
    var sum = 0;
    //
    for (var i=rut.length - 1; i >=0; i--) {
        var d = rut.charAt(i)
        sum += new Number(d)*secuencia[rut.length - (i + 1)];
    };
    // sum mod 11
    var rest = 11 - (sum % 11);
    // si es 11, retorna 0, sino si es 10 retorna K,
    // en caso contrario retorna el numero
    return rest === 11 ? '0' : rest === 10 ? "K" : ''+rest;
};