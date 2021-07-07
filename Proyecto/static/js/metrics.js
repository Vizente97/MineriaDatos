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

    $("#analize-metric-btn").click(function(){
        var form_data = new FormData($('#file-form')[0]);
        form_data.append("metricas_options",$("#metricas_options").val());
        var cod = document.getElementById("metricas_options").value;
        if(cod == "minkowski"){
            form_data.append("p_minkowski",$("#p_minkowski").val());
        }
        $.ajax({
            url: '/metrics',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container2").css("display","block");
                var tabla = response;
                $("#tablamatriz").html(tabla);
                if( $('#table2').length){
                    $('#table2').DataTable( {
                        responsive: true
                    } );
                }
                console.log(response);
            },
            error: function(error){
                console.log(response);
            }
        });          
    });

    $('#metricas_options').on('change',function(e){
        var cod = document.getElementById("metricas_options").value;
        //alert(cod)
        if(cod == "minkowski"){
            $("#option_minkowski").css("display","block");
        }
        else{
            $("#option_minkowski").css("display","none");
        }
    });

});