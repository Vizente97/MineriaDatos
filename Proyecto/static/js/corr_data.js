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

    $("#file-analize-btn").click(function(){
        var form_data = new FormData($('#file-form')[0]);
        $.ajax({
            url: '/data_analize',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container").css("display","block");
                var tabla = response[0];
                var shape = "<p><b>Shape: </b>"+response[1]+"</p>";
                var type = "<p><b>Types: </b>"+response[2]+"</p>";
                var nulos = "<br><p>"+response[3]+"</p>";
                var realcion = response[4];
                var imagen_heap = response[5];
                var imagen_heap_inf = response[6];
                var imagen_heap_sup = response[7];
                var labels = response[8];
                $("#tabla_data").html(tabla);
                $("#tamano_data").html(shape);
                $("#data_type").html(type);
                $("#data_nulos").html(nulos);
                $("#relation_values").html(realcion);
                $("#heap").html(imagen_heap);
                $("#heap_inf").html(imagen_heap_inf);
                $("#heap_sup").html(imagen_heap_sup);
                $("#abscisa_options").html(labels);
                $("#ordenada_options").html(labels);
                if( $('#table1').length){
                    $('#table1').DataTable( {
                        responsive: true
                    } );
                }
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

    $("#graph-btn").click(function(){
        var form = new FormData();
        form.append("abscisa_options",$("#abscisa_options").val());
        form.append("ordenada_options",$("#ordenada_options").val());
        $.ajax({
            url: '/graph_corr',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container2").css("display","block");
                var img = response;
                $("#img_two_data").html(img);
                console.log(response);
            },
            error: function(error){
                console.log(response);
            }
        });          
    });

    

});