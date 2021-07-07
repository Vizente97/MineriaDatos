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

    $("#file-btn-pca").click(function(){
        var form_data = new FormData($('#file-form')[0]);
        $.ajax({
            url: '/data_table_pca',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container").css("display","block");
                $("#features-container2").css("display","none");
                $("#features-container3").css("display","none");
                $("#features-container4").css("display","none");
                var tabla = response[0];
                var columnas = response[1];
                $("#tabla_data").html(tabla);
                if( $('#table1').length){
                    $('#table1').DataTable( {
                        responsive: true
                    } );
                }
                $("#columns_options").html(columnas);
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

    $("#eliminar-y-btn").click(function(){
        var form = new FormData();
        form.append("columns_options",$("#columns_options").val());
        $.ajax({
            url: '/update_data',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container2").css("display","block");
                var tabla = response[0];
                var columnas = response[1];
                $("#tabla_actual").html(tabla);
                if( $('#table2').length){
                    $('#table2').DataTable( {
                        responsive: true
                    } );
                }
                $("#columns_options").html(columnas);
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

    $("#normalize-btn").click(function(){
        $.ajax({
            url: '/normalize_data',
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container3").css("display","block");
                var tabla = response;
                $("#tabla_normalizada").html(tabla);
                if( $('#table3').length){
                    $('#table3').DataTable( {
                        responsive: true
                    } );
                }
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

    $("#component-btn").click(function(){
        var form = new FormData();
        form.append("components",$("#components").val());
        $.ajax({
            url: '/pca_analysis',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container4").css("display","block");
                var tabla = response[0];
                var eugenvalues = "<p><b>Eugenvalues: </b>"+response[1]+"</p>";
                var varianza = "<p><b>Varianza acumulada: </b>"+response[2]+"</p>";
                var img = response[3];
                var tabla2 = response[4];
                var tabla3 = response[5];
                var tabla4 = response[6];
                var tabla5 = response[7];
                $("#tabla_componentes").html(tabla);
                if( $('#table4').length){
                    $('#table4').DataTable( {
                        responsive: true
                    } );
                }
                $("#componentes_no_abs").html(tabla2);
                if( $('#table5').length){
                    $('#table5').DataTable( {
                        responsive: true
                    } );
                }
                $("#componentes_abs").html(tabla3);
                if( $('#table6').length){
                    $('#table6').DataTable( {
                        responsive: true
                    } );
                }
                $("#cargas_abs").html(tabla4);
                if( $('#table7').length){
                    $('#table7').DataTable( {
                        responsive: true
                    } );
                }
                $("#cargas_no_abs").html(tabla5);
                if( $('#table8').length){
                    $('#table8').DataTable( {
                        responsive: true
                    } );
                }
                $("#eigenvalues").html(eugenvalues);
                $("#varianza").html(varianza);
                $("#img_varianza").html(img);
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

});