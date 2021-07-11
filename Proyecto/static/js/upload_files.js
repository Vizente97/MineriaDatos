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

    $("#file-btn").click(function(){
        $("#js-loader").css("display","block");
        var form_data = new FormData($('#file-form')[0]);
        $.ajax({
            url: '/data_table',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container").css("display","block");
                var tabla = response[0];
                var columnas = response[1];
                $("#tabla_data").html(tabla);
                if( $('#table1').length){
                    console.log("Entre aquí");
                    $('#table1').DataTable( {
                        responsive: true
                    } );
                }
                $("#column_options").html(columnas);
                $("#js-loader").css("display","none");
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

    $('#column_options').on('change',function(e){
        $("#js-loader").css("display","block");
        var form = new FormData();
        form.append("column_options",$("#column_options").val());
        $.ajax({
            url: '/data_filas',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                var filas = response;
                $("#fila_options").html(filas);
                $("#js-loader").css("display","none");
            },
            error: function(error){
                console.log(response);
            }
        });
    });

    $("#analize-btn").click(function(){
        $("#js-loader").css("display","block");
        var form = new FormData();
        form.append("column_options",$("#column_options").val());
        form.append("fila_options",$("#fila_options").val());
        $.ajax({
            url: '/data_file',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container2").css("display","block");
                var tamano = "<p><b>Shape: </b>"+response[0]+"</p>";
                var types = "<p><b>Types: </b>"+response[1]+"</p>";
                var nulls = "<br><p>"+response[2]+"</p>";
                var imagen = response[3];
                var tabla = response[4];
                var tabla2 = response[5];
                var imagen_heap = response[6];
                $("#tamano_data").html(tamano);
                $("#data_type").html(types);
                $("#data_nulos").html(nulls);
                $("#data_atipico").html(imagen);
                $("#resumen_atipico").html(tabla);
                $("#relation_values").html(tabla2);
                $("#heap").html(imagen_heap);
                if( $('#table2').length){
                    console.log("Entre aquí");
                    $('#table2').DataTable( {
                        responsive: true
                    } );
                }
                if( $('#table3').length){
                    console.log("Entre aquí");
                    $('#table3').DataTable( {
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

});