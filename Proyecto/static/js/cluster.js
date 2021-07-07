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

    $("#file-btn-cluster").click(function(){
        var form_data = new FormData($('#file-form')[0]);
        $.ajax({
            url: '/data_table_pca',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container").css("display","block");
                var tabla = response[0];
                var columnas = response[1];
                $("#tabla1").html(tabla);
                if( $('#table1').length){
                    $('#table1').DataTable( {
                        responsive: true
                    } );
                }
                $("#group_options").html(columnas);
                $("#x_options").html(columnas);
                $("#y_options").html(columnas);
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

    $("#graph-dispertion-btn").click(function(){
        var form = new FormData();
        form.append("group_options",$("#group_options").val());
        form.append("x_options",$("#x_options").val());
        form.append("y_options",$("#y_options").val());
        $.ajax({
            url: '/graph_dispertion',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container3").css("display","block");
                var img = response;
                $("#graph_dispersion").html(img);
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

    $("#matriz-dispertion-btn").click(function(){
        $.ajax({
            url: '/pearson',
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container4").css("display","block");
                var pearson = response[0];
                var img = response[1];
                $("#pearson").html(pearson);
                if( $('#table2').length){
                    $('#table2').DataTable( {
                        responsive: true
                    } );
                }
                console.log(response);
                $("#img_heatmap").html(img);
            },
            error: function(error){
            }
        });    
    });

});