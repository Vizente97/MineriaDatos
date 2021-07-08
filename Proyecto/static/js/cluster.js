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
                $("#features-container2").css("display","none");
                $("#features-container3").css("display","none");
                $("#features-container4").css("display","none");
                $("#features-container5").css("display","none");
                $("#features-container6").css("display","none");
                $("#features-container7").css("display","none");
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
                $("#variables_select").html("");
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
                $("#features-container5").css("display","block");
                var pearson = response[0];
                var img = response[1];
                var columnas = response[2];
                $("#pearson").html(pearson);
                if( $('#table2').length){
                    $('#table2').DataTable( {
                        responsive: true
                    } );
                }
                console.log(response);
                $("#img_heatmap").html(img);
                $("#selection_options").html(columnas);
            },
            error: function(error){
            }
        });    
    });

    $("#select-btn").click(function(){
        var form = new FormData();
        form.append("selection_options",$("#selection_options").val());
        $.ajax({
            url: '/select_variables',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                var variables = response;
                $("#variables_select").html(variables);
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

    $("#data-create-btn").click(function(){
        var form = new FormData();
        $.ajax({
            url: '/createData',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container6").css("display","block");
                var tabla = response;
                $("#newData").html(tabla);
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

    $("#kmeas-btn").click(function(){
        $.ajax({
            url: '/kmeas',
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container7").css("display","block");
                var see = response[0];
                var knee = response[1];
                var t_clusters = response[2];
                var g_clusters = response[3];
                var t_centroides = response[4];
                var graph_3d = response[5];
                $("#sse").html(see);
                $("#kneepoint").html(knee);
                $("#table_cluster").html(t_clusters);
                if( $('#table4').length){
                    $('#table4').DataTable( {
                        responsive: true
                    } );
                }
                $("#graph_cluster").html(g_clusters);
                $("#tableCentroide").html(t_centroides);
                if( $('#table5').length){
                    $('#table5').DataTable( {
                        responsive: true
                    } );
                }
                $("#3D").html(graph_3d);
                console.log(response);
            },
            error: function(error){
            }
        });    
    });

});