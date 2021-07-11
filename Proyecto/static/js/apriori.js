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

    $("#file-apriori-btn").click(function(){
        $("#js-loader").css("display","block");
        var form_data = new FormData($('#file-form')[0]);
        form_data.append("header_options",$("#header_options").val())
        $.ajax({
            url: '/data_table_apriori',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container").css("display","block");
                var tabla = response;
                $("#tabla_data").html(tabla);
                if( $('#table1').length){
                    $('#table1').DataTable( {
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

    $("#apriori-btn").click(function(){
        $("#js-loader").css("display","block");
        var form_data = new FormData();
        form_data.append("soporte",$("#soporte").val())
        form_data.append("confianza",$("#confianza").val())
        form_data.append("elevacion",$("#elevacion").val())
        $.ajax({
            url: '/reglas_apriori',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container2").css("display","block");
                var tabla = response;
                $("#tabla_configuraciones").html(tabla);
                if( $('#table2').length){
                    $('#table2').DataTable( {
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