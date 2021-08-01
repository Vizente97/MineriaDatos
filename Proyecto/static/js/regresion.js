$(document).ready(function () {
    if ($('input[type=file]')[0].files.length){
        $(".custom-file-label").html($('input[type=file]')[0].files[0].name);
    }
    
   $('#file').on('change',function(e){
        //get the file name
        var fileName = e.target.files[0].name;
        //replace the "Choose a file" label
        $(this).next('.custom-file-label').html(fileName);
    });

    $("#file-btn-regresion").click(function(){
        $("#js-loader").css("display","block");
        var form_data = new FormData($('#file-form')[0]);
        $.ajax({
            url: '/data_table_regresion',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container").css("display","block");
                $("#features-container2").css("display","none");
                $("#features-container3").css("display","none");
                $("#features-container4").css("display","none");
                $("#features-container5").css("display","none");
                $("#features-container6").css("display","none");
                $("#features-container7").css("display","none");
                var tabla = response[0];
                var tabla2 = response[1];
                $("#tabla1").html(tabla);
                if( $('#table1').length){
                    $('#table1').DataTable( {
                        responsive: true
                    } );
                }
                $("#tabla2").html(tabla2);
                if( $('#table2').length){
                    $('#table2').DataTable( {
                        responsive: true
                    } );
                }
                $("#js-loader").css("display","none");
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

    $("#new-data-regresion-btn").click(function(){
        $("#js-loader").css("display","block");
        var form = new FormData();
        valores = []
        $('#table2 tr').each(function (i, row) {
            row = $(this).closest('tr');
            var cbkbox = $("td:eq(0) input:checked", row).val();
            if(cbkbox == 'on'){
                //var valor = row.find('td:eq(1)').text();
                //valores.push(valor)
            }
            else{
                var valor = row.find('td:eq(1)').text();
                valores.push(valor)
            }
        });
        form.append("seleccionados",valores)
        $.ajax({
            url: '/regresion_data',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container2").css("display","block");
                $("#features-container3").css("display","block");
                var tabla = response[0];
                var tabla2 = response[1];
                var y_valores = response[2];
                $("#tabla3").html(tabla);
                if( $('#table3').length){
                    $('#table3').DataTable( {
                        responsive: true
                    } );
                }
                $("#tabla4").html(tabla2);
                if( $('#table4').length){
                    $('#table4').DataTable( {
                        responsive: true
                    } );
                }
                $("#y_pronosticar").html(y_valores);
                $("#js-loader").css("display","none");
            },
            error: function(error){
            }
        });   
    });

    $("#model-btn").click(function(){
        //$("#js-loader").css("display","block");
        var form = new FormData();
        valores = []
        $('#table4 tr').each(function (i, row) {
            row = $(this).closest('tr');
            var cbkbox = $("td:eq(0) input:checked", row).val();
            if(cbkbox == 'on'){
                var valor = row.find('td:eq(1)').text();
                valores.push(valor)
            }
        });
        form.append("seleccionados",valores);
        form.append("y_pronosticar",$("#y_pronosticar").val());
        form.append("test",$("#test").val());
        $.ajax({
            url: '/regresion_model',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container4").css("display","block");
                var exactitud = response[0];
                var tabla = response[1];
                $("#exactitud").html(exactitud);
                $("#tabla5").html(tabla);
                if( $('#table5').length){
                    $('#table5').DataTable( {
                        responsive: true
                    } );
                }
                //$("#js-loader").css("display","none");
            },
            error: function(error){
            }
        });   
    });

});