$(document).ready(function () {
    var keys = [];

    $("#load-model-btn").click(function(){
        $("#js-loader").css("display","block");
        var form = new FormData();
        form.append("modelo",$("#modelos").val());
        $.ajax({
            url: '/load_model',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container").css("display","block");
                var inputs = response[0];
                keys = response[1];;
                $("#input_values").html(inputs);
                $("#js-loader").css("display","none");
                console.log(response)
            },
            error: function(error){
            }
        });   
    });

    $("#use-model-btn").click(function(){
        $("#js-loader").css("display","block");
        var form = new FormData();
        for (var i = 0; i < keys.length; i++) {
            var mjs = "#"+keys[i].toString();
            form.append(keys[i].toString(),$(mjs).val());
        }
        $.ajax({
            url: '/use_model',
            data: form,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                $("#features-container2").css("display","block");
                var predict = response;
                $("#resultado").html(predict);
                $("#js-loader").css("display","none");
            },
            error: function(error){
            }
        });   
    });

});