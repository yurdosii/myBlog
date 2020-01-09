$(document).ready(function() {
    var form = $('#form_interpreter');
    var result = $('#textarea_result');

    form.on('submit', function(e) {
        e.preventDefault()

        var data = {};
        var csrf_token = $("#form_interpreter [name='csrfmiddlewaretoken']").val();
        var url = form.attr("action");
        var code = $("#form_interpreter textarea").val();

        data["csrfmiddlewaretoken"] = csrf_token;
        data["code"] = code;

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                console.log("OK");
                console.log(data);
                result.val(data.result)
            },
            error: function() {
                console.log("error");
            }
        });
    });
});